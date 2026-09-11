"""
CA-M023 acceptance tests — Deterministic Portfolio Yield Gating.

Proof classes covered:
- schema/contract binding;
- positive progression;
- fail-closed insufficiency with structured gap reports;
- independent diversity hard gates;
- deterministic receipts;
- frozen contract dependence;
- false-proof countercase: a high aggregate yield score cannot unlock assembly;
- integration boundary: costly assembly callback is not invoked on failure.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SERVICE_SRC = ROOT / "services/interview-intelligence/src"
if str(SERVICE_SRC) not in sys.path:
    sys.path.insert(0, str(SERVICE_SRC))

from cae_interview_intelligence.yield_gating import (  # noqa: E402
    FrozenContentPortfolioContract,
    INVARIANT_ID,
    MANDATE_ID,
    NarrativeYieldMetrics,
    POLICY_VERSION,
    YieldGateBlockedError,
    evaluate_yield,
    gate_downstream_media_assembly,
    metrics_from_candidates,
)


def contract() -> FrozenContentPortfolioContract:
    return FrozenContentPortfolioContract.from_payload(
        contract_id="content-portfolio:test",
        contract_version="1.0.0",
        min_viable_candidates=16,
        min_evidence_backed_ratio=0.90,
        min_unique_audience_islands=8,
        min_unique_tensions=6,
        min_unique_guest_territories=4,
        min_unique_archetypes=4,
    )


def passing_metrics() -> NarrativeYieldMetrics:
    return NarrativeYieldMetrics(
        viable_candidates=16,
        evidence_backed_candidates=16,
        unique_audience_islands=8,
        unique_tensions=6,
        unique_guest_territories=4,
        unique_archetypes=4,
    )


def test_mandate_constants_and_contract_hash_binding() -> None:
    assert MANDATE_ID == "CA-M023"
    assert INVARIANT_ID == "FR-023"
    assert POLICY_VERSION == "CA-M023-PORTFOLIO-YIELD-V1"
    c = contract()
    assert len(c.contract_sha256) == 64
    assert c.contract_sha256 == FrozenContentPortfolioContract.from_payload(
        contract_id=c.contract_id,
        contract_version=c.contract_version,
        min_viable_candidates=c.min_viable_candidates,
        min_evidence_backed_ratio=c.min_evidence_backed_ratio,
        min_unique_audience_islands=c.min_unique_audience_islands,
        min_unique_tensions=c.min_unique_tensions,
        min_unique_guest_territories=c.min_unique_guest_territories,
        min_unique_archetypes=c.min_unique_archetypes,
    ).contract_sha256


def test_positive_path_unlocks_when_every_contract_gate_passes() -> None:
    decision = evaluate_yield(passing_metrics(), contract())
    assert decision.allowed is True
    assert decision.report.passed is True
    assert decision.report.gaps == ()
    assert decision.report.metrics["evidence_backed_ratio"] == 1.0


@pytest.mark.parametrize(
    ("metric", "minimum"),
    [
        ("viable_candidates", 16),
        ("unique_audience_islands", 8),
        ("unique_tensions", 6),
        ("unique_guest_territories", 4),
        ("unique_archetypes", 4),
    ],
)
def test_each_contract_metric_is_independently_hard_gated(
    metric: str,
    minimum: int,
) -> None:
    values = passing_metrics().__dict__.copy()
    values[metric] = minimum - 1
    if metric == "viable_candidates":
        values["evidence_backed_candidates"] = minimum - 1
    decision = evaluate_yield(NarrativeYieldMetrics(**values), contract())

    assert decision.allowed is False
    assert len(decision.report.gaps) == 1
    assert decision.report.gaps[0]["metric"] == metric
    assert decision.report.gaps[0]["deficit"] == 1


def test_evidence_backed_ratio_is_hard_gated_even_with_sufficient_count_and_diversity() -> None:
    metrics = NarrativeYieldMetrics(
        viable_candidates=20,
        evidence_backed_candidates=17,
        unique_audience_islands=8,
        unique_tensions=6,
        unique_guest_territories=4,
        unique_archetypes=4,
    )
    decision = evaluate_yield(metrics, contract())
    assert decision.allowed is False
    assert decision.report.gaps == (
        {
            "code": "YIELD_EVIDENCE_BACKED_RATIO",
            "metric": "evidence_backed_ratio",
            "observed": 0.85,
            "required": 0.9,
            "deficit": 0.05,
        },
    )


def test_multiple_gaps_are_returned_structured_and_fail_closed() -> None:
    metrics = NarrativeYieldMetrics(
        viable_candidates=12,
        evidence_backed_candidates=8,
        unique_audience_islands=3,
        unique_tensions=2,
        unique_guest_territories=1,
        unique_archetypes=2,
    )
    decision = evaluate_yield(metrics, contract())

    assert decision.allowed is False
    assert {
        gap["code"] for gap in decision.report.gaps
    } == {
        "YIELD_MIN_VIABLE_CANDIDATES",
        "YIELD_EVIDENCE_BACKED_RATIO",
        "YIELD_DIVERSITY_AUDIENCE_ISLANDS",
        "YIELD_DIVERSITY_TENSIONS",
        "YIELD_DIVERSITY_GUEST_TERRITORIES",
        "YIELD_DIVERSITY_ARCHETYPES",
    }
    payload = decision.report.to_dict()
    assert payload["contract_sha256"] == contract().contract_sha256
    assert payload["passed"] is False


def test_receipt_is_deterministic_for_identical_contract_and_metrics() -> None:
    first = evaluate_yield(passing_metrics(), contract()).report.to_dict()
    second = evaluate_yield(passing_metrics(), contract()).report.to_dict()
    assert first == second
    assert first["receipt_sha256"] == second["receipt_sha256"]


def test_contract_requirements_are_authoritative_not_module_defaults() -> None:
    higher_contract = FrozenContentPortfolioContract.from_payload(
        contract_id="content-portfolio:test",
        contract_version="1.1.0",
        min_viable_candidates=20,
        min_evidence_backed_ratio=1.0,
        min_unique_audience_islands=10,
        min_unique_tensions=8,
        min_unique_guest_territories=5,
        min_unique_archetypes=5,
    )
    decision = evaluate_yield(passing_metrics(), higher_contract)
    assert decision.allowed is False
    assert {gap["metric"] for gap in decision.report.gaps} == {
        "viable_candidates",
        "unique_audience_islands",
        "unique_tensions",
        "unique_guest_territories",
        "unique_archetypes",
    }


def test_false_proof_high_aggregate_yield_score_does_not_unlock_assembly() -> None:
    # A convincing 0.95 "yield score" is intentionally not an input to the gate.
    # The same portfolio still fails because the contract's diversity evidence fails.
    metrics = NarrativeYieldMetrics(
        viable_candidates=16,
        evidence_backed_candidates=16,
        unique_audience_islands=2,
        unique_tensions=6,
        unique_guest_territories=4,
        unique_archetypes=4,
    )
    decision = evaluate_yield(metrics, contract())
    assert decision.allowed is False
    assert any(
        gap["code"] == "YIELD_DIVERSITY_AUDIENCE_ISLANDS"
        for gap in decision.report.gaps
    )


def test_downstream_assembly_callback_is_not_called_when_yield_fails() -> None:
    calls: list[str] = []

    def expensive_assembly() -> str:
        calls.append("render")
        return "assembled"

    metrics = NarrativeYieldMetrics(
        viable_candidates=15,
        evidence_backed_candidates=15,
        unique_audience_islands=8,
        unique_tensions=6,
        unique_guest_territories=4,
        unique_archetypes=4,
    )
    with pytest.raises(YieldGateBlockedError) as exc_info:
        gate_downstream_media_assembly(
            metrics,
            contract(),
            expensive_assembly,
        )
    assert calls == []
    assert exc_info.value.report.passed is False
    assert exc_info.value.report.gaps[0]["metric"] == "viable_candidates"


def test_downstream_assembly_callback_runs_after_a_passing_gate() -> None:
    calls: list[str] = []

    def expensive_assembly() -> str:
        calls.append("render")
        return "assembled"

    result = gate_downstream_media_assembly(
        passing_metrics(),
        contract(),
        expensive_assembly,
    )
    assert result == "assembled"
    assert calls == ["render"]


def test_metrics_from_candidates_uses_existing_portfolio_diversity_dimensions() -> None:
    class Candidate:
        def __init__(self, index: int) -> None:
            self.provenance = type(
                "P",
                (),
                {"source_refs": [f"src:{index}"]},
            )()
            self.upstream_hypothesis_refs = [f"hyp:{index}"]
            self._sig = {
                "audience_island": f"island:{index % 2}",
                "tension": f"tension:{index % 3}",
                "guest_territory": f"territory:{index % 4}",
                "archetype": f"archetype:{index % 5}",
            }

        def get_diversity_signature(self) -> dict[str, str]:
            return self._sig

    candidates = [Candidate(i) for i in range(10)]
    metrics = metrics_from_candidates(
        candidates,
        evidence_backed_predicate=lambda candidate: bool(candidate.provenance.source_refs),
    )
    assert metrics.viable_candidates == 10
    assert metrics.evidence_backed_candidates == 10
    assert metrics.evidence_backed_ratio == 1.0
    assert metrics.unique_audience_islands == 2
    assert metrics.unique_tensions == 3
    assert metrics.unique_guest_territories == 4
    assert metrics.unique_archetypes == 5


def test_invalid_contract_cannot_be_constructed() -> None:
    with pytest.raises(ValueError, match="contract_sha256"):
        FrozenContentPortfolioContract(
            contract_id="content-portfolio:test",
            contract_version="1.0.0",
            min_viable_candidates=16,
            min_evidence_backed_ratio=0.9,
            min_unique_audience_islands=8,
            min_unique_tensions=6,
            min_unique_guest_territories=4,
            min_unique_archetypes=4,
            contract_sha256="not-a-hash",
        )

    valid = contract()
    with pytest.raises(ValueError, match="does not match"):
        FrozenContentPortfolioContract(
            contract_id=valid.contract_id,
            contract_version=valid.contract_version,
            min_viable_candidates=valid.min_viable_candidates + 1,
            min_evidence_backed_ratio=valid.min_evidence_backed_ratio,
            min_unique_audience_islands=valid.min_unique_audience_islands,
            min_unique_tensions=valid.min_unique_tensions,
            min_unique_guest_territories=valid.min_unique_guest_territories,
            min_unique_archetypes=valid.min_unique_archetypes,
            contract_sha256=valid.contract_sha256,
        )
