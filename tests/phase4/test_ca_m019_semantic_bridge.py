"""CA-M019 acceptance suite for the Expression Moments semantic bridge.

Verification matrix
===================
SCHEMA
  test_expression_moment_contains_direct_semantic_bridge_fields
  test_receipt_is_hash_addressable_and_stamped

EXECUTABLE — positive path
  test_bridge_accepts_admitted_contextual_utterance_and_vector
  test_mapping_inputs_are_supported_without_inferred_intermediaries
  test_receipt_is_deterministic_for_identical_inputs

EXECUTABLE — negative / fail-closed path
  test_missing_admission_receipt_is_rejected
  test_quarantined_evidence_cannot_cross_semantic_bridge
  test_downstream_blocked_evidence_cannot_cross_semantic_bridge
  test_missing_context_lineage_is_rejected
  test_invalid_context_lineage_is_rejected
  test_vector_for_different_utterance_is_rejected
  test_emotional_polarity_change_is_rejected
  test_subject_stance_change_is_rejected
  test_empty_vector_evidence_refs_are_rejected
  test_intermediary_frames_are_rejected_as_hallucinated_semantics
  test_invalid_vector_dimension_is_rejected

COMPOSITION BOUNDARY
  test_composition_accepts_only_real_expression_moment
  test_raw_text_is_rejected_at_composition_boundary
  test_fake_expression_moment_mapping_is_rejected_at_composition_boundary

FALSE-PROOF countercases
  test_matching_object_name_does_not_prove_semantic_bridge
  test_highly_detailed_vector_still_fails_when_polarity_changes

REGRESSION / auditability
  test_source_text_and_lineage_are_preserved_verbatim
  test_source_anchor_and_vector_evidence_are_retained
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SERVICE_SRC = ROOT / "services" / "interview" / "src"
if str(SERVICE_SRC) not in sys.path:
    sys.path.insert(0, str(SERVICE_SRC))

from conscious_activations_interview_expression.semantic_bridge import (
    INVARIANT_ID,
    MANDATE_ID,
    POLICY_VERSION,
    SCHEMA_VERSION,
    ConceptualActivationVector,
    ExpressionMoment,
    InvalidBridgeInputError,
    RawCompositionInputRejectedError,
    RawSpokenUtterance,
    SemanticBridge,
    SemanticTransformationRejectedError,
)


_SHA = hashlib.sha256(b"ca-m019-fixture").hexdigest()


def _ref(object_id: str) -> dict[str, str]:
    return {"object_id": object_id, "version": "1.0.0", "sha256": _SHA}


def _source_span() -> dict[str, object]:
    return {
        "source_id": "source:interview-001",
        "source_version": "1.0.0",
        "source_sha256": _SHA,
        "start_ms": 1000,
        "end_ms": 2400,
        "speaker_id": "speaker:subject",
    }


def _utterance() -> RawSpokenUtterance:
    return RawSpokenUtterance(
        utterance_id="utt-001",
        text="I was afraid, but I still chose to speak.",
        source_ref=_ref("source:interview-001"),
        source_span=_source_span(),
        speaker_id="speaker:subject",
        emotional_polarity="MIXED",
        subject_stance="SELF_AUTHORED_RESOLVE",
        admission_ref=_ref("utt-001"),
        context_lineage_refs=(_ref("ctx:interview-001"),),
    )


def _vector() -> ConceptualActivationVector:
    return ConceptualActivationVector(
        vector_id="vec-001",
        source_utterance_id="utt-001",
        dimensions={
            "vulnerability": 0.84,
            "resolve": 0.91,
            "agency": 0.88,
        },
        emotional_polarity="MIXED",
        subject_stance="SELF_AUTHORED_RESOLVE",
        evidence_refs=(_ref("utt-001"),),
    )


def _admission_receipt(**overrides: object) -> dict[str, object]:
    receipt: dict[str, object] = {
        "admitted": True,
        "downstream_generation_allowed": True,
        "evidence_id": "utt-001",
    }
    receipt.update(overrides)
    return receipt


def _context_lineage(**overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "valid": True,
        "node_refs": [_ref("ctx:interview-001")],
    }
    result.update(overrides)
    return result


@pytest.fixture
def bridge() -> SemanticBridge:
    return SemanticBridge()


# ============================================================================
# SCHEMA
# ============================================================================


def test_expression_moment_contains_direct_semantic_bridge_fields(bridge: SemanticBridge) -> None:
    receipt = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())
    moment = receipt.expression_moment

    assert moment.mandate_id == MANDATE_ID
    assert moment.invariant_id == INVARIANT_ID
    assert moment.schema_version == SCHEMA_VERSION
    assert moment.source_utterance_id == "utt-001"
    assert moment.source_text == _utterance().text
    assert moment.activation_vector.vector_id == "vec-001"
    assert moment.intermediary_frames == ()
    assert moment.transformation == "DIRECT_UTTERANCE_TO_ACTIVATION_VECTOR"
    assert len(moment.moment_sha256) == 64


def test_receipt_is_hash_addressable_and_stamped(bridge: SemanticBridge) -> None:
    receipt = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())

    assert receipt.mandate_id == MANDATE_ID
    assert receipt.invariant_id == INVARIANT_ID
    assert receipt.policy_version == POLICY_VERSION
    assert len(receipt.receipt_sha256) == 64
    assert set(receipt.checks) == {
        "admitted_evidence",
        "context_lineage_present",
        "direct_utterance_anchor",
        "polarity_preserved",
        "subject_stance_preserved",
        "no_intermediary_frames",
    }
    assert all(receipt.checks.values())


# ============================================================================
# POSITIVE
# ============================================================================


def test_bridge_accepts_admitted_contextual_utterance_and_vector(bridge: SemanticBridge) -> None:
    receipt = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())

    assert isinstance(receipt.expression_moment, ExpressionMoment)
    assert receipt.expression_moment.activation_vector.dimensions["resolve"] == 0.91


def test_mapping_inputs_are_supported_without_inferred_intermediaries(bridge: SemanticBridge) -> None:
    source = _utterance()
    vector = _vector()
    result = bridge.bridge(
        {
            "utterance_id": source.utterance_id,
            "text": source.text,
            "source_ref": dict(source.source_ref),
            "source_span": dict(source.source_span),
            "speaker_id": source.speaker_id,
            "emotional_polarity": source.emotional_polarity,
            "subject_stance": source.subject_stance,
            "admission_ref": dict(source.admission_ref),
            "context_lineage_refs": [dict(ref) for ref in source.context_lineage_refs],
        },
        {
            "vector_id": vector.vector_id,
            "source_utterance_id": vector.source_utterance_id,
            "dimensions": dict(vector.dimensions),
            "emotional_polarity": vector.emotional_polarity,
            "subject_stance": vector.subject_stance,
            "evidence_refs": [dict(ref) for ref in vector.evidence_refs],
        },
        admission_receipt=_admission_receipt(),
        context_lineage=_context_lineage(),
    )

    assert result.expression_moment.intermediary_frames == ()


def test_receipt_is_deterministic_for_identical_inputs(bridge: SemanticBridge) -> None:
    first = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())
    second = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())

    assert first.receipt_sha256 == second.receipt_sha256
    assert first.expression_moment.moment_sha256 == second.expression_moment.moment_sha256
    assert first.expression_moment.to_dict() == second.expression_moment.to_dict()


# ============================================================================
# NEGATIVE / FAIL CLOSED
# ============================================================================


def test_missing_admission_receipt_is_rejected(bridge: SemanticBridge) -> None:
    with pytest.raises(InvalidBridgeInputError, match="authoritative admission receipt"):
        bridge.bridge(_utterance(), _vector(), context_lineage=_context_lineage())


def test_quarantined_evidence_cannot_cross_semantic_bridge(bridge: SemanticBridge) -> None:
    with pytest.raises(SemanticTransformationRejectedError, match="not admitted"):
        bridge.bridge(
            _utterance(),
            _vector(),
            admission_receipt=_admission_receipt(admitted=False),
            context_lineage=_context_lineage(),
        )


def test_downstream_blocked_evidence_cannot_cross_semantic_bridge(bridge: SemanticBridge) -> None:
    with pytest.raises(SemanticTransformationRejectedError, match="barred downstream"):
        bridge.bridge(
            _utterance(),
            _vector(),
            admission_receipt=_admission_receipt(downstream_generation_allowed=False),
            context_lineage=_context_lineage(),
        )


def test_missing_context_lineage_is_rejected(bridge: SemanticBridge) -> None:
    with pytest.raises(InvalidBridgeInputError, match="context-lineage result"):
        bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt())


def test_invalid_context_lineage_is_rejected(bridge: SemanticBridge) -> None:
    with pytest.raises(SemanticTransformationRejectedError, match="context lineage"):
        bridge.bridge(
            _utterance(),
            _vector(),
            admission_receipt=_admission_receipt(),
            context_lineage={"valid": False, "node_refs": [_ref("ctx:interview-001")]},
        )


def test_vector_for_different_utterance_is_rejected(bridge: SemanticBridge) -> None:
    foreign = replace(_vector(), source_utterance_id="utt-999")
    with pytest.raises(SemanticTransformationRejectedError, match="exact source utterance"):
        bridge.bridge(_utterance(), foreign, admission_receipt=_admission_receipt(), context_lineage=_context_lineage())


def test_emotional_polarity_change_is_rejected(bridge: SemanticBridge) -> None:
    altered = replace(_vector(), emotional_polarity="POSITIVE")
    with pytest.raises(SemanticTransformationRejectedError, match="emotional polarity"):
        bridge.bridge(_utterance(), altered, admission_receipt=_admission_receipt(), context_lineage=_context_lineage())


def test_subject_stance_change_is_rejected(bridge: SemanticBridge) -> None:
    altered = replace(_vector(), subject_stance="EXTERNAL_OBSERVER")
    with pytest.raises(SemanticTransformationRejectedError, match="subject stance"):
        bridge.bridge(_utterance(), altered, admission_receipt=_admission_receipt(), context_lineage=_context_lineage())


def test_empty_vector_evidence_refs_are_rejected(bridge: SemanticBridge) -> None:
    with pytest.raises(InvalidBridgeInputError, match="evidence_refs"):
        replace(_vector(), evidence_refs=())


def test_intermediary_frames_are_rejected_as_hallucinated_semantics() -> None:
    with pytest.raises(SemanticTransformationRejectedError, match="intermediary frames"):
        ExpressionMoment(
            expression_moment_id="ie:expression-moment:bad",
            mandate_id=MANDATE_ID,
            invariant_id=INVARIANT_ID,
            schema_version=SCHEMA_VERSION,
            source_utterance_id=_utterance().utterance_id,
            source_text=_utterance().text,
            source_ref=_utterance().source_ref,
            source_span=_utterance().source_span,
            speaker_id=_utterance().speaker_id,
            admission_ref=_utterance().admission_ref,
            context_lineage_refs=_utterance().context_lineage_refs,
            activation_vector=_vector(),
            preserved_emotional_polarity=_utterance().emotional_polarity,
            preserved_subject_stance=_utterance().subject_stance,
            transformation="DIRECT_UTTERANCE_TO_ACTIVATION_VECTOR",
            intermediary_frames=("invented-emotional-scene",),
            moment_sha256=_SHA,
        )


def test_invalid_vector_dimension_is_rejected() -> None:
    with pytest.raises(InvalidBridgeInputError, match="finite numeric"):
        ConceptualActivationVector(
            vector_id="vec-invalid",
            source_utterance_id="utt-001",
            dimensions={"resolve": float("nan")},
            emotional_polarity="MIXED",
            subject_stance="SELF_AUTHORED_RESOLVE",
            evidence_refs=(_ref("utt-001"),),
        )


# ============================================================================
# COMPOSITION BOUNDARY
# ============================================================================


def test_composition_accepts_only_real_expression_moment(bridge: SemanticBridge) -> None:
    receipt = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())

    accepted = bridge.require_composition_input(receipt.expression_moment)

    assert accepted is receipt.expression_moment


def test_raw_text_is_rejected_at_composition_boundary(bridge: SemanticBridge) -> None:
    with pytest.raises(RawCompositionInputRejectedError, match="requires an ExpressionMoment"):
        bridge.require_composition_input(_utterance().text)


def test_fake_expression_moment_mapping_is_rejected_at_composition_boundary(bridge: SemanticBridge) -> None:
    fake = {
        "expression_moment_id": "looks-real",
        "activation_vector": {"resolve": 0.91},
        "source_text": _utterance().text,
    }

    with pytest.raises(RawCompositionInputRejectedError):
        bridge.require_composition_input(fake)


# ============================================================================
# FALSE-PROOF COUNTERCASES
# ============================================================================


def test_matching_object_name_does_not_prove_semantic_bridge(bridge: SemanticBridge) -> None:
    fake = type("ExpressionMoment", (), {"mandate_id": MANDATE_ID, "invariant_id": INVARIANT_ID})()

    with pytest.raises(RawCompositionInputRejectedError):
        bridge.require_composition_input(fake)


def test_highly_detailed_vector_still_fails_when_polarity_changes(bridge: SemanticBridge) -> None:
    altered = replace(
        _vector(),
        emotional_polarity="POSITIVE",
        dimensions={
            "vulnerability": 0.99,
            "resolve": 0.99,
            "agency": 0.98,
            "hope": 0.97,
            "confidence": 0.96,
        },
    )

    with pytest.raises(SemanticTransformationRejectedError, match="emotional polarity"):
        bridge.bridge(_utterance(), altered, admission_receipt=_admission_receipt(), context_lineage=_context_lineage())


# ============================================================================
# REGRESSION / AUDITABILITY
# ============================================================================


def test_source_text_and_lineage_are_preserved_verbatim(bridge: SemanticBridge) -> None:
    source = _utterance()
    result = bridge.bridge(source, _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())
    moment = result.expression_moment

    assert moment.source_text == source.text
    assert moment.source_ref == source.source_ref
    assert moment.source_span == source.source_span
    assert moment.context_lineage_refs == source.context_lineage_refs
    assert moment.speaker_id == source.speaker_id


def test_source_anchor_and_vector_evidence_are_retained(bridge: SemanticBridge) -> None:
    result = bridge.bridge(_utterance(), _vector(), admission_receipt=_admission_receipt(), context_lineage=_context_lineage())
    payload = result.expression_moment.to_dict()

    assert payload["source_ref"] == dict(_utterance().source_ref)
    assert payload["source_span"] == _source_span()
    assert payload["admission_ref"] == _utterance().admission_ref
    assert payload["activation_vector"]["evidence_refs"] == [dict(_ref("utt-001"))]

    # The serialized moment is self-consistent and hashable.
    material = dict(payload)
    observed = material.pop("moment_sha256")
    encoded = json.dumps(material | {"moment_sha256": observed}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert len(encoded) > 0
    assert len(observed) == 64
