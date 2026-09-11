"""CA-M017 acceptance suite for fail-closed, multi-dimensional evidence admission.

The suite intentionally exercises the repository import path used by the root
Phase 4 tests. It treats ``EvidenceAdmissionBoundary.admit`` as the authoritative
runtime boundary and verifies both admission receipts and the generation barrier.

Per mandate, these tests are included but are not executed by the implementation
agent in this bundle build.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import pytest

from conscious_activations_interview_expression.evidence_admission import (
    AdmissionState,
    DEFAULT_MIN_ADMISSION_CONFIDENCE,
    DEFAULT_MIN_CORROBORATION_COUNT,
    DEFAULT_MIN_VERBATIM_FIDELITY,
    EvidenceAdmissionBoundary,
    EvidenceAdmissionPolicy,
    EvidenceCandidate,
    EvidenceType,
    EvidenceGenerationBlockedError,
    InvalidEvidenceCandidateError,
)


@pytest.fixture
def boundary() -> EvidenceAdmissionBoundary:
    return EvidenceAdmissionBoundary()


def admitted_candidate(
    *,
    evidence_id: str = "ev-m017-001",
    evidence_type: EvidenceType = EvidenceType.QUOTE,
    confidence: float = DEFAULT_MIN_ADMISSION_CONFIDENCE,
    corroboration: int = DEFAULT_MIN_CORROBORATION_COUNT,
    fidelity: float = DEFAULT_MIN_VERBATIM_FIDELITY,
    fidelity_pass: bool = True,
    epistemic_legality: bool = True,
    identity_fit: bool = True,
    domain_fit: bool = True,
    downstream_generation_requested: bool = True,
    **metadata: Any,
) -> EvidenceCandidate:
    return EvidenceCandidate(
        evidence_id=evidence_id,
        evidence_type=evidence_type,
        admission_confidence=confidence,
        corroboration_count=corroboration,
        verbatim_fidelity=fidelity,
        fidelity_pass=fidelity_pass,
        epistemic_legality=epistemic_legality,
        identity_fit=identity_fit,
        domain_fit=domain_fit,
        source_ref="workspace://m017/source-001",
        downstream_generation_requested=downstream_generation_requested,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# 1. Positive authoritative-boundary path
# ---------------------------------------------------------------------------


def test_authoritative_boundary_admits_all_three_evidence_types(boundary: EvidenceAdmissionBoundary) -> None:
    for evidence_type in EvidenceType:
        receipt = boundary.admit(admitted_candidate(evidence_id=f"{evidence_type.value}-001", evidence_type=evidence_type))

        assert receipt.admitted is True
        assert receipt.state is AdmissionState.ADMITTED
        assert receipt.downstream_generation_allowed is True
        assert receipt.quarantine_reason_codes == ()
        assert set(receipt.gates) == {
            "confidence",
            "corroboration",
            "verbatim_fidelity",
            "fidelity",
            "epistemic_legality",
            "identity_fit",
            "domain_fit",
        }
        assert all(gate.passed for gate in receipt.gates.values())
        assert len(receipt.receipt_sha256) == 64


def test_positive_receipt_is_hash_addressable_and_contains_policy(boundary: EvidenceAdmissionBoundary) -> None:
    receipt = boundary.admit(admitted_candidate())
    payload = receipt.to_dict()

    assert payload["mandate_id"] == "CA-M017"
    assert payload["invariant_id"] == "FR-EV-001"
    assert payload["policy_version"] == "CA-M017-EVIDENCE-ADMISSION-V1"
    assert payload["threshold_policy"]["min_admission_confidence"] == 0.80
    assert payload["threshold_policy"]["min_corroboration_count"] == 2
    assert payload["threshold_policy"]["min_verbatim_fidelity"] == 0.95


# ---------------------------------------------------------------------------
# 2. User-facing quantitative gates: one failed dimension must quarantine
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("field", "value", "reason_code"),
    [
        ("admission_confidence", DEFAULT_MIN_ADMISSION_CONFIDENCE - 0.01, "BELOW_MINIMUM_ADMISSION_CONFIDENCE"),
        ("corroboration_count", DEFAULT_MIN_CORROBORATION_COUNT - 1, "INSUFFICIENT_CORROBORATION"),
        ("verbatim_fidelity", DEFAULT_MIN_VERBATIM_FIDELITY - 0.01, "BELOW_MINIMUM_VERBATIM_FIDELITY"),
    ],
)
def test_each_quantitative_gate_quarantines_fail_closed(
    boundary: EvidenceAdmissionBoundary,
    field: str,
    value: Any,
    reason_code: str,
) -> None:
    candidate = replace(admitted_candidate(), **{field: value})
    receipt = boundary.admit(candidate)

    assert receipt.admitted is False
    assert receipt.state is AdmissionState.QUARANTINED
    assert receipt.downstream_generation_allowed is False
    assert reason_code in receipt.quarantine_reason_codes
    gate_name = {"admission_confidence": "confidence", "corroboration_count": "corroboration"}.get(field, field)
    assert receipt.gates[gate_name].passed is False


def test_minimum_thresholds_are_inclusive(boundary: EvidenceAdmissionBoundary) -> None:
    receipt = boundary.admit(admitted_candidate())

    assert receipt.gates["confidence"].passed is True
    assert receipt.gates["corroboration"].passed is True
    assert receipt.gates["verbatim_fidelity"].passed is True


# ---------------------------------------------------------------------------
# 3. Constitutional FR-EVID-001 dimensions are also unanimous hard gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("field", "reason_code"),
    [
        ("fidelity_pass", "FIDELITY_GATE_FAILED"),
        ("epistemic_legality", "EPISTEMIC_LEGALITY_GATE_FAILED"),
        ("identity_fit", "IDENTITY_FIT_GATE_FAILED"),
        ("domain_fit", "DOMAIN_FIT_GATE_FAILED"),
    ],
)
def test_each_constitutional_boolean_gate_is_non_compensable(
    boundary: EvidenceAdmissionBoundary,
    field: str,
    reason_code: str,
) -> None:
    candidate = replace(admitted_candidate(), **{field: False})
    receipt = boundary.admit(candidate)

    assert receipt.admitted is False
    assert receipt.state is AdmissionState.QUARANTINED
    assert reason_code in receipt.quarantine_reason_codes
    assert all(
        gate.passed
        for name, gate in receipt.gates.items()
        if name != {
            "fidelity_pass": "fidelity",
            "epistemic_legality": "epistemic_legality",
            "identity_fit": "identity_fit",
            "domain_fit": "domain_fit",
        }[field]
    )


def test_high_confidence_cannot_rescue_a_failed_other_gate(boundary: EvidenceAdmissionBoundary) -> None:
    candidate = admitted_candidate(
        confidence=0.99,
        corroboration=9,
        fidelity=0.99,
        fidelity_pass=False,
        epistemic_legality=True,
        identity_fit=True,
        domain_fit=True,
    )

    receipt = boundary.admit(candidate)

    assert receipt.admitted is False
    assert receipt.state is AdmissionState.QUARANTINED
    assert receipt.gates["confidence"].passed is True
    assert receipt.gates["corroboration"].passed is True
    assert receipt.gates["verbatim_fidelity"].passed is True
    assert receipt.gates["fidelity"].passed is False


# ---------------------------------------------------------------------------
# 4. Missing/invalid dimensions fail closed instead of defaulting true
# ---------------------------------------------------------------------------


def test_mapping_boundary_rejects_missing_gate_input_without_defaulting_true(boundary: EvidenceAdmissionBoundary) -> None:
    payload = {
        "evidence_id": "ev-m017-missing",
        "evidence_type": "claim",
        "admission_confidence": 0.99,
        "corroboration_count": 9,
        "verbatim_fidelity": 0.99,
        "fidelity_pass": True,
        "epistemic_legality": True,
        "identity_fit": True,
        # domain_fit intentionally absent
        "source_ref": "workspace://m017/source-001",
    }

    with pytest.raises(InvalidEvidenceCandidateError) as exc_info:
        boundary.admit(payload)

    assert exc_info.value.context["missing_fields"] == ["domain_fit"]


def test_boolean_gate_must_not_accept_truthy_non_boolean_value(boundary: EvidenceAdmissionBoundary) -> None:
    payload = admitted_candidate()
    with pytest.raises(InvalidEvidenceCandidateError):
        EvidenceCandidate(**{**_candidate_kwargs(payload), "identity_fit": 1})


# ---------------------------------------------------------------------------
# 5. Downstream-generation barrier
# ---------------------------------------------------------------------------


def test_quarantined_evidence_is_barred_from_downstream_generation(boundary: EvidenceAdmissionBoundary) -> None:
    receipt = boundary.admit(
        admitted_candidate(
            evidence_type=EvidenceType.CLAIM,
            confidence=0.79,
            downstream_generation_requested=True,
        )
    )

    with pytest.raises(EvidenceGenerationBlockedError) as exc_info:
        boundary.require_generation_admission(receipt)

    assert exc_info.value.context["reason_code"] == "QUARANTINED_EVIDENCE"
    assert receipt.downstream_generation_allowed is False


def test_admit_for_generation_requires_a_passing_receipt(boundary: EvidenceAdmissionBoundary) -> None:
    with pytest.raises(EvidenceGenerationBlockedError):
        boundary.admit_for_generation(
            admitted_candidate(
                evidence_type=EvidenceType.MEDIA,
                corroboration=1,
                downstream_generation_requested=True,
            )
        )


def test_generation_requires_authoritative_receipt(boundary: EvidenceAdmissionBoundary) -> None:
    with pytest.raises(EvidenceGenerationBlockedError) as exc_info:
        boundary.require_generation_admission({"admitted": True})

    assert exc_info.value.context["reason_code"] == "MISSING_AUTHORITATIVE_RECEIPT"


def test_admitted_receipt_can_cross_generation_barrier(boundary: EvidenceAdmissionBoundary) -> None:
    receipt = boundary.admit(admitted_candidate(downstream_generation_requested=True))
    boundary.require_generation_admission(receipt)
    assert receipt.state is AdmissionState.ADMITTED


# ---------------------------------------------------------------------------
# 6. Fail-closed validation and policy boundaries
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "candidate_mutation",
    [
        {"admission_confidence": float("nan")},
        {"admission_confidence": float("inf")},
        {"verbatim_fidelity": -0.01},
        {"verbatim_fidelity": 1.01},
        {"corroboration_count": -1},
        {"corroboration_count": True},
    ],
)
def test_invalid_quantitative_inputs_are_rejected_fail_closed(
    candidate_mutation: dict[str, Any],
) -> None:
    base = admitted_candidate()
    with pytest.raises(InvalidEvidenceCandidateError):
        EvidenceCandidate(**{**_candidate_kwargs(base), **candidate_mutation})


def test_policy_cannot_create_invalid_permissive_thresholds() -> None:
    with pytest.raises(ValueError):
        EvidenceAdmissionPolicy(min_admission_confidence=1.01)
    with pytest.raises(ValueError):
        EvidenceAdmissionPolicy(min_verbatim_fidelity=-0.01)
    with pytest.raises(ValueError):
        EvidenceAdmissionPolicy(min_corroboration_count=-1)
    with pytest.raises(ValueError):
        EvidenceAdmissionPolicy(min_corroboration_count=True)


# ---------------------------------------------------------------------------
# 7. False-proof countercase: shape + scalar confidence is not enough
# ---------------------------------------------------------------------------


def test_false_proof_case_four_booleans_plus_high_confidence_is_still_rejected() -> None:
    boundary = EvidenceAdmissionBoundary()
    misleading = {
        "evidence_id": "ev-m017-false-proof",
        "evidence_type": "quote",
        "admission_confidence": 0.97,
        "corroboration_count": 0,
        "verbatim_fidelity": 0.91,
        "fidelity_pass": True,
        "epistemic_legality": True,
        "identity_fit": True,
        "domain_fit": True,
        "source_ref": "workspace://m017/source-001",
        "downstream_generation_requested": True,
    }

    receipt = boundary.admit(misleading)

    assert receipt.admitted is False
    assert receipt.state is AdmissionState.QUARANTINED
    assert receipt.gates["confidence"].passed is True
    assert receipt.gates["fidelity"].passed is True
    assert receipt.gates["epistemic_legality"].passed is True
    assert receipt.gates["identity_fit"].passed is True
    assert receipt.gates["domain_fit"].passed is True
    assert receipt.gates["corroboration"].passed is False
    assert receipt.gates["verbatim_fidelity"].passed is False


# ---------------------------------------------------------------------------
# 8. Per-type coverage and audit receipt stability
# ---------------------------------------------------------------------------


def test_media_quote_and_claim_have_distinct_auditable_receipts(boundary: EvidenceAdmissionBoundary) -> None:
    receipts = [
        boundary.admit(admitted_candidate(evidence_id=f"{kind.value}-stable", evidence_type=kind))
        for kind in EvidenceType
    ]

    assert {receipt.evidence_type for receipt in receipts} == set(EvidenceType)
    assert len({receipt.receipt_sha256 for receipt in receipts}) == 3
    assert all(receipt.admitted for receipt in receipts)


def test_repeat_evaluation_is_deterministic_for_same_candidate(boundary: EvidenceAdmissionBoundary) -> None:
    candidate = admitted_candidate(evidence_id="ev-m017-deterministic")

    first = boundary.admit(candidate)
    second = boundary.admit(candidate)

    assert first.to_dict() == second.to_dict()
    assert first.receipt_sha256 == second.receipt_sha256


# ---------------------------------------------------------------------------
# Local helper avoids depending on dataclass __dict__ for slots instances.
# ---------------------------------------------------------------------------


def _candidate_kwargs(candidate: EvidenceCandidate) -> dict[str, Any]:
    return {
        "evidence_id": candidate.evidence_id,
        "evidence_type": candidate.evidence_type,
        "admission_confidence": candidate.admission_confidence,
        "corroboration_count": candidate.corroboration_count,
        "verbatim_fidelity": candidate.verbatim_fidelity,
        "fidelity_pass": candidate.fidelity_pass,
        "epistemic_legality": candidate.epistemic_legality,
        "identity_fit": candidate.identity_fit,
        "domain_fit": candidate.domain_fit,
        "source_ref": candidate.source_ref,
        "downstream_generation_requested": candidate.downstream_generation_requested,
        "metadata": dict(candidate.metadata),
    }
