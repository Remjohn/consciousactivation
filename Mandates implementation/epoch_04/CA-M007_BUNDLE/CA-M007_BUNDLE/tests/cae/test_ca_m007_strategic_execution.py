"""
CA-M007 / FR-007 / INV-ACT-001 executable evidence.

Coverage:
- valid derivation from Guest Genesis + Audience Tensions + CONVERGED receipt
- exact revision/digest ancestry binding
- mandatory signed operator intent
- operator-intent signature tamper rejection
- execution-target mismatch rejection
- raw-topic/manual insertion rejection
- missing lineage rejection
- stale upstream/convergence receipt rejection
- cross-workspace rejection
- payload digest integrity on downstream admission
- positive downstream admission after full ancestry verification

DO NOT RUN TESTS PER MANDATE INSTRUCTIONS — this file is test-definition only.
"""

from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from ca_runtime.convergence_gate import (
    AudienceTensionsRef,
    ConvergenceGate,
    GuestGenesisRef,
)
from ca_runtime.strategic_execution import (
    CrossWorkspaceStrategicExecutionError,
    InvalidLineageError,
    InvalidOperatorIntentError,
    MissingLineageError,
    OperatorIntent,
    RawTopicInsertionError,
    StaleConvergenceReceiptError,
    StrategicExecutionPayload,
    require_admitted_strategic_execution,
)


WS = "ws-ca-m007"


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def genesis(*, workspace_id: str = WS, revision: str = "gg-r1", digest: str | None = None) -> GuestGenesisRef:
    return GuestGenesisRef(
        workspace_id=workspace_id,
        territory_id="territory-ca-m007",
        revision_id=revision,
        sha256_digest=digest or sha(f"genesis:{workspace_id}:{revision}"),
        ratified_state="TERRITORY_RATIFIED",
        wrong_reading_locks=("do not flatten directness into hostility",),
        vocabulary_boundaries=("precision", "friction-tested clarity"),
    )


def tensions(*, workspace_id: str = WS, revision: str = "t-r1", digest: str | None = None) -> AudienceTensionsRef:
    return AudienceTensionsRef(
        workspace_id=workspace_id,
        audience_id="audience-ca-m007",
        revision_id=revision,
        sha256_digest=digest or sha(f"tensions:{workspace_id}:{revision}"),
        tension_state="TENSIONS_ACTIVE",
        tension_count=2,
        active_tension_labels=("autonomy-vs-accountability", "speed-vs-precision"),
    )


def intent(execution_id: str = "exec-ca-m007") -> OperatorIntent:
    return OperatorIntent.sign(
        intent_id="intent-ca-m007-001",
        workspace_id=WS,
        operator_id="operator-001",
        action="ADMIT_STRATEGIC_EXECUTION",
        rationale="Approve derivative strategic execution from converged context.",
        target_execution_id=execution_id,
        signed_at_utc="2026-09-08T06:30:00+00:00",
    )


def valid_payload() -> tuple[StrategicExecutionPayload, GuestGenesisRef, AudienceTensionsRef, object]:
    gg = genesis()
    at = tensions()
    receipt = ConvergenceGate().evaluate(
        workspace_id=WS,
        guest_genesis=gg,
        audience_tensions=at,
    )
    payload = StrategicExecutionPayload.derive(
        execution_id="exec-ca-m007",
        workspace_id=WS,
        strategic_objective="Convert the approved collision into a governed interview strategy.",
        transformation_vector={
            "recognition_target": "make the surviving edge explicit",
            "execution_mode": "structured_elicitation",
        },
        genesis=gg,
        tensions=at,
        convergence_receipt=receipt,
        operator_intent=intent(),
    )
    return payload, gg, at, receipt


def test_ca_m007_valid_derivation_contains_full_upstream_ancestry() -> None:
    payload, gg, at, receipt = valid_payload()

    assert payload.program_id == "activative_strategic_execution"
    assert payload.genesis.object_id == gg.territory_id
    assert payload.genesis.revision_id == gg.revision_id
    assert payload.genesis.sha256_digest == gg.sha256_digest
    assert payload.tensions.object_id == at.audience_id
    assert payload.tensions.revision_id == at.revision_id
    assert payload.tensions.sha256_digest == at.sha256_digest
    assert payload.convergence.receipt_id == receipt.receipt_id
    assert payload.convergence.convergence_digest == receipt.convergence_digest
    assert payload.operator_intent.verify() is True
    assert payload.operator_intent.target_execution_id == payload.execution_id


def test_ca_m007_exact_parent_revisions_and_digests_are_persisted_in_object() -> None:
    payload, gg, at, receipt = valid_payload()

    assert payload.convergence.guest_genesis_revision_id == gg.revision_id
    assert payload.convergence.guest_genesis_sha256 == gg.sha256_digest
    assert payload.convergence.audience_tensions_revision_id == at.revision_id
    assert payload.convergence.audience_tensions_sha256 == at.sha256_digest
    assert payload.convergence.gate_version == receipt.gate_version


def test_ca_m007_unsigned_operator_intent_cannot_be_instantiated() -> None:
    gg = genesis()
    at = tensions()
    receipt = ConvergenceGate().evaluate(
        workspace_id=WS,
        guest_genesis=gg,
        audience_tensions=at,
    )

    unsigned = OperatorIntent(
        intent_id="intent-ca-m007-unsigned",
        workspace_id=WS,
        operator_id="operator-001",
        action="ADMIT_STRATEGIC_EXECUTION",
        rationale="Not signed.",
        target_execution_id="exec-ca-m007",
        signed_at_utc="2026-09-08T06:30:00+00:00",
        signature_sha256="",
    )

    with pytest.raises(InvalidOperatorIntentError, match="signature is invalid"):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=gg,
            tensions=at,
            convergence_receipt=receipt,
            operator_intent=unsigned,
        )


def test_ca_m007_tampered_operator_intent_signature_is_rejected() -> None:
    payload, gg, at, receipt = valid_payload()
    tampered = replace(payload.operator_intent, rationale="Different intent")
    tampered_payload = replace(payload, operator_intent=tampered)

    with pytest.raises(InvalidOperatorIntentError, match="signature"):
        tampered_payload.verify_integrity(
            genesis=gg,
            tensions=at,
            convergence_receipt=receipt,
        )


def test_ca_m007_operator_intent_must_target_exact_execution_object() -> None:
    gg = genesis()
    at = tensions()
    receipt = ConvergenceGate().evaluate(workspace_id=WS, guest_genesis=gg, audience_tensions=at)
    wrong_target = intent(execution_id="different-execution")

    with pytest.raises(InvalidOperatorIntentError, match="not signed for this execution_id"):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=gg,
            tensions=at,
            convergence_receipt=receipt,
            operator_intent=wrong_target,
        )


def test_ca_m007_raw_topic_insertion_is_explicitly_rejected() -> None:
    with pytest.raises(RawTopicInsertionError, match="cannot be instantiated from a raw topic"):
        StrategicExecutionPayload.from_raw_topic(topic="Interview about leadership")


def test_ca_m007_missing_genesis_is_fail_closed() -> None:
    at = tensions()
    receipt = ConvergenceGate().evaluate(
        workspace_id=WS,
        guest_genesis=genesis(),
        audience_tensions=at,
    )

    with pytest.raises(MissingLineageError, match="Guest Genesis ancestry"):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=None,  # type: ignore[arg-type]
            tensions=at,
            convergence_receipt=receipt,
            operator_intent=intent(),
        )


def test_ca_m007_missing_tensions_is_fail_closed() -> None:
    gg = genesis()
    receipt = ConvergenceGate().evaluate(
        workspace_id=WS,
        guest_genesis=gg,
        audience_tensions=tensions(),
    )

    with pytest.raises(MissingLineageError, match="Audience Tensions ancestry"):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=gg,
            tensions=None,  # type: ignore[arg-type]
            convergence_receipt=receipt,
            operator_intent=intent(),
        )


def test_ca_m007_missing_convergence_receipt_is_fail_closed() -> None:
    gg = genesis()
    at = tensions()

    with pytest.raises(MissingLineageError, match="Convergence receipt ancestry"):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=gg,
            tensions=at,
            convergence_receipt=None,  # type: ignore[arg-type]
            operator_intent=intent(),
        )


def test_ca_m007_non_converged_receipt_is_not_an_admission_token() -> None:
    payload, gg, at, receipt = valid_payload()
    blocked = replace(receipt, status=type(receipt.status).BLOCKED)

    with pytest.raises(InvalidLineageError, match="must be CONVERGED"):
        StrategicExecutionPayload.derive(
            execution_id=payload.execution_id,
            workspace_id=WS,
            strategic_objective=payload.strategic_objective,
            transformation_vector=payload.transformation_vector,
            genesis=gg,
            tensions=at,
            convergence_receipt=blocked,
            operator_intent=intent(payload.execution_id),
        )


def test_ca_m007_stale_genesis_digest_is_rejected() -> None:
    payload, gg, at, receipt = valid_payload()
    stale_gg = genesis(revision=gg.revision_id, digest=sha("mutated-genesis"))

    with pytest.raises(StaleConvergenceReceiptError):
        payload.verify_integrity(
            genesis=stale_gg,
            tensions=at,
            convergence_receipt=receipt,
        )


def test_ca_m007_stale_tensions_revision_is_rejected() -> None:
    payload, gg, at, receipt = valid_payload()
    stale_at = tensions(revision="t-r2")

    with pytest.raises(StaleConvergenceReceiptError):
        payload.verify_integrity(
            genesis=gg,
            tensions=stale_at,
            convergence_receipt=receipt,
        )


def test_ca_m007_cross_workspace_lineage_is_rejected() -> None:
    gg = genesis(workspace_id="ws-other")
    at = tensions(workspace_id=WS)
    receipt = ConvergenceGate().evaluate(
        workspace_id="ws-other",
        guest_genesis=gg,
        audience_tensions=tensions(workspace_id="ws-other"),
    )

    with pytest.raises(CrossWorkspaceStrategicExecutionError):
        StrategicExecutionPayload.derive(
            execution_id="exec-ca-m007",
            workspace_id=WS,
            strategic_objective="Govern the execution from approved context.",
            transformation_vector={"mode": "structured_elicitation"},
            genesis=gg,
            tensions=at,
            convergence_receipt=receipt,
            operator_intent=intent(),
        )


def test_ca_m007_downstream_admission_reverifies_full_ancestry() -> None:
    payload, gg, at, receipt = valid_payload()

    admitted = require_admitted_strategic_execution(
        payload,
        genesis=gg,
        tensions=at,
        convergence_receipt=receipt,
    )

    assert admitted is payload
    assert admitted.payload_sha256
    assert len(admitted.payload_sha256) == 64


def test_ca_m007_payload_digest_detects_mutation() -> None:
    payload, gg, at, receipt = valid_payload()
    mutated = replace(
        payload,
        strategic_objective="A different strategic objective that was not signed into this object.",
    )

    with pytest.raises(InvalidLineageError, match="payload digest"):
        require_admitted_strategic_execution(
            mutated,
            genesis=gg,
            tensions=at,
            convergence_receipt=receipt,
        )


def test_ca_m007_payload_serialization_exposes_complete_lineage_and_intent() -> None:
    payload, _, _, _ = valid_payload()
    data = payload.to_dict()

    assert set(("genesis", "tensions", "convergence", "operator_intent")).issubset(data)
    assert set(("object_id", "revision_id", "sha256_digest")).issubset(data["genesis"])
    assert set(("object_id", "revision_id", "sha256_digest")).issubset(data["tensions"])
    assert set(("receipt_id", "convergence_digest", "convergence_signature")).issubset(data["convergence"])
    assert set(("operator_id", "target_execution_id", "signature_sha256")).issubset(data["operator_intent"])
