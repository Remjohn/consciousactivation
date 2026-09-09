"""Acceptance tests for CA-M003 Subject Constitution lifecycle.

These tests are intentionally not executed by the execution agent per the mandate
instruction. They are the bounded evidence suite to run after applying the bundle.
"""

from __future__ import annotations

import pytest

from ca_runtime.subject_constitution import (
    AMENDMENT_AUTHORITY_SCOPE,
    AmendmentAlreadyResolvedError,
    AmendmentStatus,
    ConstitutionAlreadyExistsError,
    ConstitutionExceptionType,
    InvalidAmendmentError,
    InvalidSignatureError,
    StaleParentRevisionError,
    SubjectConstitutionAmendmentPacket,
    SubjectConstitutionLifecycle,
    UnauthorizedOperatorError,
)


SECRET = "ca-m003-test-signing-secret"
SIGNED_AT = "2026-09-08T10:00:00Z"
AMENDED_AT = "2026-09-08T10:05:00Z"


def build_lifecycle() -> SubjectConstitutionLifecycle:
    lifecycle = SubjectConstitutionLifecycle(signing_secret=SECRET)
    lifecycle.create_signed_baseline(
        subject_id="subject-001",
        source_evidence_refs=("interview:segment:001", "interview:segment:002"),
        voice_characteristics={"cadence": "measured", "energy": "warm"},
        boundaries={"forbidden_topics": ["private_family_information"]},
        validation_state={"state": "OPERATOR_VALIDATED", "confidence": "HIGH"},
        operator_id="operator-001",
        signed_at_utc=SIGNED_AT,
    )
    return lifecycle


def build_packet(
    *,
    lifecycle: SubjectConstitutionLifecycle,
    amendment_id: str = "amendment-001",
    parent_revision: int = 1,
    operator_id: str = "operator-001",
    evidence_refs: tuple[str, ...] = ("interview:segment:003",),
    exception_id: str | None = None,
) -> SubjectConstitutionAmendmentPacket:
    return SubjectConstitutionAmendmentPacket(
        amendment_id=amendment_id,
        subject_id="subject-001",
        parent_revision=parent_revision,
        proposed_voice_characteristics={"cadence": "measured", "energy": "more_direct"},
        proposed_boundaries=None,
        proposed_validation_state={"state": "OPERATOR_VALIDATED", "confidence": "HIGH"},
        reason="recent source evidence demonstrates a stable expressive shift",
        evidence_refs=evidence_refs,
        operator_id=operator_id,
        exception_id=exception_id,
    )


def test_ca_m003_01_signed_baseline_is_cryptographically_verifiable_and_immutable():
    lifecycle = build_lifecycle()
    baseline = lifecycle.current("subject-001")

    assert baseline.revision == 1
    assert baseline.status == "SIGNED"
    assert baseline.verify(SECRET) is True

    with pytest.raises(TypeError):
        baseline.voice_characteristics["energy"] = "cold"  # type: ignore[index]
    with pytest.raises(TypeError):
        baseline.boundaries["forbidden_topics"][0] = "other"  # type: ignore[index]
    with pytest.raises((AttributeError, TypeError)):
        baseline.revision = 2  # type: ignore[misc]

    baseline.require_verified(SECRET)


def test_ca_m003_02_tampering_with_signed_record_fails_verification():
    lifecycle = build_lifecycle()
    baseline = lifecycle.current("subject-001")

    tampered = type(baseline)(
        subject_id=baseline.subject_id,
        revision=baseline.revision,
        status=baseline.status,
        source_evidence_refs=baseline.source_evidence_refs,
        voice_characteristics={"cadence": "measured", "energy": "tampered"},
        boundaries=baseline.boundaries,
        validation_state=baseline.validation_state,
        signed_by_operator_id=baseline.signed_by_operator_id,
        signed_at_utc=baseline.signed_at_utc,
        content_sha256=baseline.content_sha256,
        signature_sha256=baseline.signature_sha256,
    )

    assert tampered.verify(SECRET) is False
    with pytest.raises(InvalidSignatureError):
        tampered.require_verified(SECRET)


def test_ca_m003_03_exception_is_recorded_without_auto_mutating_baseline():
    lifecycle = build_lifecycle()
    baseline_before = lifecycle.current("subject-001")
    exception = lifecycle.record_exception(
        subject_id="subject-001",
        exception_type=ConstitutionExceptionType.VOICE_DRIFT,
        description="Recent interview expression departs from the signed cadence baseline.",
        evidence_refs=("interview:segment:010",),
        observed_at_utc=AMENDED_AT,
        detected_by="voice-drift-detector",
        exception_id="exception-001",
    )

    baseline_after = lifecycle.current("subject-001")
    assert exception.exception_id == "exception-001"
    assert baseline_after.revision == baseline_before.revision == 1
    assert baseline_after.signature_sha256 == baseline_before.signature_sha256


def test_ca_m003_04_valid_operator_amendment_creates_new_version_and_receipt():
    lifecycle = build_lifecycle()
    exception = lifecycle.record_exception(
        subject_id="subject-001",
        exception_type=ConstitutionExceptionType.VOICE_DRIFT,
        description="Observed stable expressive shift.",
        evidence_refs=("interview:segment:020",),
        observed_at_utc=AMENDED_AT,
        detected_by="operator-review-queue",
        exception_id="exception-020",
    )
    packet = build_packet(lifecycle=lifecycle, exception_id=exception.exception_id)
    lifecycle.submit_amendment(packet)

    revised, receipt = lifecycle.approve_amendment(
        amendment_id=packet.amendment_id,
        operator_id="operator-001",
        authority_scope=AMENDMENT_AUTHORITY_SCOPE,
        decided_at_utc=AMENDED_AT,
    )

    assert revised.revision == 2
    assert revised.parent_revision == 1
    assert revised.amendment_receipt_id == receipt.receipt_id
    assert revised.verify(SECRET) is True
    assert receipt.verify(SECRET) is True
    assert receipt.parent_revision == 1
    assert receipt.resulting_revision == 2
    assert receipt.exception_id == "exception-020"
    assert receipt.operator_id == "operator-001"
    assert receipt.evidence_refs == ("interview:segment:003",)
    assert receipt.parent_signature_sha256 != revised.signature_sha256

    history = lifecycle.history("subject-001")
    assert [item.revision for item in history] == [1, 2]
    assert len(lifecycle.receipts_for_subject("subject-001")) == 1


def test_ca_m003_05_stale_parent_is_fail_closed():
    lifecycle = build_lifecycle()
    first = build_packet(lifecycle=lifecycle, amendment_id="amendment-first")
    lifecycle.submit_amendment(first)
    lifecycle.approve_amendment(
        amendment_id=first.amendment_id,
        operator_id="operator-001",
        authority_scope=AMENDMENT_AUTHORITY_SCOPE,
        decided_at_utc=AMENDED_AT,
    )

    stale = build_packet(lifecycle=lifecycle, amendment_id="amendment-stale", parent_revision=1)
    with pytest.raises(StaleParentRevisionError):
        lifecycle.submit_amendment(stale)


def test_ca_m003_06_missing_operator_authority_is_fail_closed():
    lifecycle = build_lifecycle()
    packet = build_packet(lifecycle=lifecycle)
    lifecycle.submit_amendment(packet)

    with pytest.raises(UnauthorizedOperatorError):
        lifecycle.approve_amendment(
            amendment_id=packet.amendment_id,
            operator_id="operator-001",
            authority_scope="MODEL_SUGGESTION",
            decided_at_utc=AMENDED_AT,
        )

    assert lifecycle.current("subject-001").revision == 1
    assert lifecycle.amendment(packet.amendment_id).status is AmendmentStatus.PENDING


def test_ca_m003_07_amendment_requires_evidence():
    lifecycle = build_lifecycle()
    with pytest.raises(InvalidAmendmentError):
        build_packet(lifecycle=lifecycle, evidence_refs=())


def test_ca_m003_08_approval_requires_packet_operator_identity():
    lifecycle = build_lifecycle()
    packet = build_packet(lifecycle=lifecycle, operator_id="operator-001")
    lifecycle.submit_amendment(packet)

    with pytest.raises(UnauthorizedOperatorError):
        lifecycle.approve_amendment(
            amendment_id=packet.amendment_id,
            operator_id="operator-002",
            authority_scope=AMENDMENT_AUTHORITY_SCOPE,
            decided_at_utc=AMENDED_AT,
        )

    assert lifecycle.current("subject-001").revision == 1


def test_ca_m003_09_history_is_preserved_and_direct_baseline_replacement_is_not_an_api():
    lifecycle = build_lifecycle()
    baseline = lifecycle.current("subject-001")
    assert lifecycle.history("subject-001") == (baseline,)

    with pytest.raises(ConstitutionAlreadyExistsError):
        lifecycle.create_signed_baseline(
            subject_id="subject-001",
            source_evidence_refs=("interview:other",),
            voice_characteristics={"cadence": "fast"},
            boundaries={},
            validation_state={"state": "DRAFT"},
            operator_id="operator-001",
            signed_at_utc=SIGNED_AT,
        )


def test_ca_m003_10_approved_amendment_cannot_be_approved_twice():
    lifecycle = build_lifecycle()
    packet = build_packet(lifecycle=lifecycle)
    lifecycle.submit_amendment(packet)
    lifecycle.approve_amendment(
        amendment_id=packet.amendment_id,
        operator_id="operator-001",
        authority_scope=AMENDMENT_AUTHORITY_SCOPE,
        decided_at_utc=AMENDED_AT,
    )

    with pytest.raises(AmendmentAlreadyResolvedError):
        lifecycle.approve_amendment(
            amendment_id=packet.amendment_id,
            operator_id="operator-001",
            authority_scope=AMENDMENT_AUTHORITY_SCOPE,
            decided_at_utc=AMENDED_AT,
        )


def test_ca_m003_11_rejected_amendment_leaves_signed_baseline_unchanged():
    lifecycle = build_lifecycle()
    packet = build_packet(lifecycle=lifecycle, amendment_id="amendment-reject")
    lifecycle.submit_amendment(packet)

    rejected = lifecycle.reject_amendment(amendment_id=packet.amendment_id, operator_id="operator-001")
    assert rejected.status is AmendmentStatus.REJECTED
    assert lifecycle.current("subject-001").revision == 1
    assert lifecycle.receipts_for_subject("subject-001") == ()
