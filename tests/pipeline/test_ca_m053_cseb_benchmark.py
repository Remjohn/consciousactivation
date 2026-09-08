"""CA-M053 CSEB golden benchmark certification tests.

Evidence classes:
- TEST: executable assertions below.
- SCHEMA/EXECUTABLE: receipt shape and signature verification through cseb_suite.
- OPERATOR_DECISION_REQUIRED: final mandate disposition remains external to tests.

The suite deliberately includes the false-proof countercase from INV-BENCH-001:
a perfect benchmark score plus an apparently valid 64-character dummy hash does
not authorize routing without a current signed certification receipt.
"""

from datetime import datetime, timedelta, timezone
import json

import pytest

# Import the bounded benchmark module directly so this mandate test does not
# require unrelated runtime adapters or their optional external dependencies.
import importlib.util
import sys
from pathlib import Path

_CSEB_PATH = (
    Path(__file__).resolve().parents[2]
    / "services"
    / "pipeline"
    / "src"
    / "cmf_pipeline"
    / "benchmarks"
    / "cseb_suite.py"
)
_CSEB_SPEC = importlib.util.spec_from_file_location("cae_m053_cseb_suite", _CSEB_PATH)
assert _CSEB_SPEC is not None and _CSEB_SPEC.loader is not None
_CSEB_MODULE = importlib.util.module_from_spec(_CSEB_SPEC)
sys.modules[_CSEB_SPEC.name] = _CSEB_MODULE
_CSEB_SPEC.loader.exec_module(_CSEB_MODULE)

BENCHMARK_ID = _CSEB_MODULE.BENCHMARK_ID
BENCHMARK_REVISION = _CSEB_MODULE.BENCHMARK_REVISION
DEFAULT_GOLDEN_CASES = _CSEB_MODULE.DEFAULT_GOLDEN_CASES
GOLDEN_DATASET_REVISION = _CSEB_MODULE.GOLDEN_DATASET_REVISION
CSEBBenchmarkSuite = _CSEB_MODULE.CSEBBenchmarkSuite
BenchmarkCaseValidationError = _CSEB_MODULE.BenchmarkCaseValidationError
BenchmarkToleranceError = _CSEB_MODULE.BenchmarkToleranceError
CertificationExpiredError = _CSEB_MODULE.CertificationExpiredError
CertificationMismatchError = _CSEB_MODULE.CertificationMismatchError
CertificationRequiredError = _CSEB_MODULE.CertificationRequiredError
CertificationRoutingGate = _CSEB_MODULE.CertificationRoutingGate
InvalidCertificationSignatureError = _CSEB_MODULE.InvalidCertificationSignatureError
ModelCertificationReceipt = _CSEB_MODULE.ModelCertificationReceipt


SIGNING_SECRET = "ca-m053-test-only-signing-secret"


@pytest.fixture()
def suite() -> CSEBBenchmarkSuite:
    return CSEBBenchmarkSuite()


@pytest.fixture()
def perfect_outputs() -> dict[str, dict]:
    return {
        "SEM-001-QUOTE-EXACTNESS": {
            "evidence": {
                "quote": "We reduced onboarding from five days to one.",
                "speaker": "source_subject",
            }
        },
        "SEM-002-PROVENANCE-FIDELITY": {
            "provenance": {"source_ref": "evidence-42", "start_ms": 615000}
        },
        "GOV-001-REFUSE-UNAUTHORIZED-TOOL": {
            "governance": {"refused": True, "executed_forbidden_action": False}
        },
        "GOV-002-SCHEMA-COMPLIANCE": {
            "schema": {"valid": True, "unknown_fields_count": 0}
        },
        "OPS-001-LATENCY-BOUND": {
            "operation": {"completed": True, "latency_ms": 5000}
        },
        "OPS-002-RETRY-BOUND": {
            "operation": {"retry_count": 1, "recovery_path_used": False}
        },
        "ECO-001-ACCEPTED-COST": {
            "economics": {"accepted": True, "cost_per_accepted_usd": 0.05}
        },
        "ECO-002-TOKEN-DISCIPLINE": {
            "economics": {"cost_observation_available": True, "completion_tokens": 1200}
        },
        "HUM-001-OPERATOR-ACCEPTANCE": {
            "human": {"operator_accepted": True, "substantive_correction": False}
        },
        "HUM-002-TIME-TO-CORRECTION": {
            "human": {"review_completed": True, "time_to_correction_seconds": 30}
        },
    }


def _issue_receipt(suite: CSEBBenchmarkSuite, perfect_outputs: dict) -> ModelCertificationReceipt:
    return suite.certify(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
        signing_secret=SIGNING_SECRET,
        issued_at=datetime(2026, 9, 8, 18, 0, tzinfo=timezone.utc),
    )


def test_default_golden_dataset_covers_all_five_cseb_dimensions(suite: CSEBBenchmarkSuite) -> None:
    assert len(DEFAULT_GOLDEN_CASES) == 10
    assert {case.dimension for case in suite.cases} == {
        "semantic",
        "governance",
        "operational",
        "economic",
        "human",
    }
    assert all(sum(case.dimension == dim for case in suite.cases) >= 2 for dim in {
        "semantic",
        "governance",
        "operational",
        "economic",
        "human",
    })


def test_perfect_candidate_is_certifiable_across_all_strict_bounds(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    result = suite.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    )
    assert result.passed is True
    assert result.overall_score_bps == 10_000
    assert result.dataset_sha256 != "a" * 64
    assert len(result.dataset_sha256) == 64
    assert all(item.score_bps == 10_000 for item in result.dimensions)


def test_single_semantic_deviation_fails_strict_zero_tolerance(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    perfect_outputs["SEM-001-QUOTE-EXACTNESS"]["evidence"]["quote"] = (
        "We reduced onboarding from five days."
    )
    result = suite.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    )
    semantic = next(item for item in result.dimensions if item.dimension == "semantic")
    assert semantic.score_bps == 7_500
    assert semantic.passed is False
    assert result.passed is False
    with pytest.raises(BenchmarkToleranceError):
        suite.certify(
            model_id="grok-test",
            model_version="2026.09.08",
            candidate_outputs=perfect_outputs,
            signing_secret=SIGNING_SECRET,
        )


def test_missing_and_unknown_case_ids_fail_closed(suite: CSEBBenchmarkSuite, perfect_outputs: dict) -> None:
    outputs = dict(perfect_outputs)
    outputs.pop("HUM-002-TIME-TO-CORRECTION")
    outputs["UNKNOWN"] = {}
    with pytest.raises(BenchmarkCaseValidationError):
        suite.evaluate(model_id="grok-test", model_version="2026.09.08", candidate_outputs=outputs)


def test_certification_receipt_is_bound_to_model_and_revisions(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    receipt.verify(
        signing_secret=SIGNING_SECRET,
        expected_model_id="grok-test",
        expected_model_version="2026.09.08",
        now=datetime(2026, 9, 8, 19, 0, tzinfo=timezone.utc),
    )
    assert receipt.schema_version
    assert receipt.benchmark_id == BENCHMARK_ID
    assert receipt.benchmark_revision == BENCHMARK_REVISION
    assert receipt.golden_dataset_revision == GOLDEN_DATASET_REVISION
    assert receipt.overall_score_bps == 10_000
    assert receipt.signature_algorithm == "HMAC-SHA256"
    assert len(receipt.signature) == 64


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_id", "other-model"),
        ("model_version", "other-version"),
    ],
)
def test_receipt_model_identity_mismatch_blocks_routing(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict, field: str, value: str
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    kwargs = {
        "model_id": "grok-test",
        "model_version": "2026.09.08",
    }
    kwargs[field] = value
    with pytest.raises(CertificationMismatchError):
        CertificationRoutingGate.require(
            receipt,
            signing_secret=SIGNING_SECRET,
            model_id=kwargs["model_id"],
            model_version=kwargs["model_version"],
        )


def test_receipt_signature_tampering_is_rejected(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    tampered = ModelCertificationReceipt(
        **{**receipt.to_dict(), "signature": "b" * 64}
    )
    with pytest.raises(InvalidCertificationSignatureError):
        tampered.verify(
            signing_secret=SIGNING_SECRET,
            expected_model_id="grok-test",
            expected_model_version="2026.09.08",
        )


def test_expired_receipt_is_rejected(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    with pytest.raises(CertificationExpiredError):
        receipt.verify(
            signing_secret=SIGNING_SECRET,
            expected_model_id="grok-test",
            expected_model_version="2026.09.08",
            now=datetime(2026, 10, 9, 18, 0, tzinfo=timezone.utc),
        )


def test_dataset_revision_mismatch_is_rejected(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    with pytest.raises(CertificationMismatchError):
        CertificationRoutingGate.require(
            receipt,
            signing_secret=SIGNING_SECRET,
            model_id="grok-test",
            model_version="2026.09.08",
            golden_dataset_revision="CSEB-GOLDEN-FUTURE.v99",
        )


def test_no_receipt_blocks_routing_even_for_perfect_score(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    result = suite.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    )
    assert result.passed is True

    with pytest.raises(CertificationRequiredError):
        CertificationRoutingGate.require(
            None,
            signing_secret=SIGNING_SECRET,
            model_id="grok-test",
            model_version="2026.09.08",
        )


def test_false_proof_dummy_hash_plus_perfect_score_is_rejected(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    """INV-BENCH-001 counterexample: score and 64-char dummy hash are not authority."""
    result = suite.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    )
    assert result.overall_score_bps == 10_000
    fake = {
        "schema_version": "cseb.model_certification_receipt.v1",
        "receipt_id": "fake",
        "benchmark_id": BENCHMARK_ID,
        "benchmark_revision": BENCHMARK_REVISION,
        "golden_dataset_revision": GOLDEN_DATASET_REVISION,
        "dataset_sha256": "a" * 64,
        "model_id": "grok-test",
        "model_version": "2026.09.08",
        "overall_score_bps": 10_000,
        "dimension_scores": {
            "semantic": 10_000,
            "governance": 10_000,
            "operational": 10_000,
            "economic": 10_000,
            "human": 10_000,
        },
        "issued_at": "2026-09-08T18:00:00+00:00",
        "expires_at": "2026-10-08T18:00:00+00:00",
        "payload_sha256": "a" * 64,
        "signature_algorithm": "HMAC-SHA256",
        "signature": "a" * 64,
    }
    with pytest.raises(InvalidCertificationSignatureError):
        CertificationRoutingGate.require(
            fake,
            signing_secret=SIGNING_SECRET,
            model_id="grok-test",
            model_version="2026.09.08",
        )


def test_routing_succeeds_only_with_valid_current_receipt(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    admitted = CertificationRoutingGate.require(
        receipt,
        signing_secret=SIGNING_SECRET,
        model_id="grok-test",
        model_version="2026.09.08",
        benchmark_revision=BENCHMARK_REVISION,
        golden_dataset_revision=GOLDEN_DATASET_REVISION,
        now=datetime(2026, 9, 8, 18, 1, tzinfo=timezone.utc),
    )
    assert admitted.receipt_id == receipt.receipt_id


def test_receipt_round_trip_json_preserves_verifiable_signature(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    receipt = _issue_receipt(suite, perfect_outputs)
    encoded = json.dumps(receipt.to_dict(), sort_keys=True)
    decoded = ModelCertificationReceipt.from_dict(json.loads(encoded))
    decoded.verify(
        signing_secret=SIGNING_SECRET,
        expected_model_id="grok-test",
        expected_model_version="2026.09.08",
    )
    assert decoded.to_dict() == receipt.to_dict()


def test_dataset_hash_changes_when_golden_revision_changes(perfect_outputs: dict) -> None:
    first = CSEBBenchmarkSuite(golden_dataset_revision="CSEB-GOLDEN-A")
    second = CSEBBenchmarkSuite(golden_dataset_revision="CSEB-GOLDEN-B")
    assert first.dataset_sha256() != second.dataset_sha256()
    assert first.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    ).dataset_sha256 != second.evaluate(
        model_id="grok-test",
        model_version="2026.09.08",
        candidate_outputs=perfect_outputs,
    ).dataset_sha256


def test_numeric_tolerance_comparator_is_strictly_inclusive() -> None:
    cases = (
        # Both observations are exactly on the declared boundary.
        # The evaluator must not widen the bound.
        DEFAULT_GOLDEN_CASES[4],
    )
    suite = CSEBBenchmarkSuite(cases=(
        cases[0],
        DEFAULT_GOLDEN_CASES[5],
        *DEFAULT_GOLDEN_CASES[:4],
        *DEFAULT_GOLDEN_CASES[6:],
    ))
    outputs = {
        "SEM-001-QUOTE-EXACTNESS": {"evidence": {"quote": "We reduced onboarding from five days to one.", "speaker": "source_subject"}},
        "SEM-002-PROVENANCE-FIDELITY": {"provenance": {"source_ref": "evidence-42", "start_ms": 615000}},
        "GOV-001-REFUSE-UNAUTHORIZED-TOOL": {"governance": {"refused": True, "executed_forbidden_action": False}},
        "GOV-002-SCHEMA-COMPLIANCE": {"schema": {"valid": True, "unknown_fields_count": 0}},
        "OPS-001-LATENCY-BOUND": {"operation": {"completed": True, "latency_ms": 5000}},
        "OPS-002-RETRY-BOUND": {"operation": {"retry_count": 1, "recovery_path_used": False}},
        "ECO-001-ACCEPTED-COST": {"economics": {"accepted": True, "cost_per_accepted_usd": 0.05}},
        "ECO-002-TOKEN-DISCIPLINE": {"economics": {"cost_observation_available": True, "completion_tokens": 1200}},
        "HUM-001-OPERATOR-ACCEPTANCE": {"human": {"operator_accepted": True, "substantive_correction": False}},
        "HUM-002-TIME-TO-CORRECTION": {"human": {"review_completed": True, "time_to_correction_seconds": 30}},
    }
    result = suite.evaluate(model_id="grok-test", model_version="2026.09.08", candidate_outputs=outputs)
    assert result.passed is True


def test_certification_cannot_be_issued_for_failed_result(
    suite: CSEBBenchmarkSuite, perfect_outputs: dict
) -> None:
    perfect_outputs["ECO-001-ACCEPTED-COST"]["economics"]["cost_per_accepted_usd"] = 0.0501
    with pytest.raises(BenchmarkToleranceError):
        suite.certify(
            model_id="grok-test",
            model_version="2026.09.08",
            candidate_outputs=perfect_outputs,
            signing_secret=SIGNING_SECRET,
        )
