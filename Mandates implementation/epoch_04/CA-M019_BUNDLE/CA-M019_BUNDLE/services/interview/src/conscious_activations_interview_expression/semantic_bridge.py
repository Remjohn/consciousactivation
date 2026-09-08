"""Fail-closed semantic bridge for CA-M019 / FR-SEM-001.

The semantic bridge is deliberately a *direct* representation boundary:

    raw spoken utterance -> conceptual activation vector -> ExpressionMoment

It does not infer an intermediate narrative frame, emotional reinterpretation,
or subject-position change. The caller must supply the already-established
conceptual activation vector and its evidence anchors. The bridge validates that
those inputs point directly to the utterance and that the transformation preserves
core emotional polarity and subject stance exactly.

The module is intentionally independent of persistence. It can therefore be used
with the interview service's existing evidence/admission and context-lineage
objects without requiring those modules to be present in the same checkout. When
such objects are supplied, the bridge validates their public admission/lineage
signals rather than recreating either contract.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any

MANDATE_ID = "CA-M019"
INVARIANT_ID = "FR-SEM-001"
SCHEMA_VERSION = "1.0.0"
POLICY_VERSION = "CA-M019-SEMANTIC-BRIDGE-V1"


class SemanticBridgeError(RuntimeError):
    """Base error for CA-M019 semantic-bridge failures."""

    code = "CA_M019_SEMANTIC_BRIDGE_ERROR"

    def __init__(self, message: str, *, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.context = dict(context or {})


class InvalidBridgeInputError(SemanticBridgeError):
    """Raised when required bridge inputs are missing or structurally invalid."""

    code = "CA_M019_INVALID_BRIDGE_INPUT"


class SemanticTransformationRejectedError(SemanticBridgeError):
    """Raised when a transformation would violate FR-SEM-001."""

    code = "CA_M019_SEMANTIC_TRANSFORMATION_REJECTED"


class RawCompositionInputRejectedError(SemanticBridgeError):
    """Raised when raw text/tokens are presented where an ExpressionMoment is required."""

    code = "CA_M019_RAW_COMPOSITION_INPUT_REJECTED"


class EmotionalPolarity(str, Enum):
    """Canonical high-level emotional polarity labels."""

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    MIXED = "MIXED"


@dataclass(frozen=True, slots=True)
class RawSpokenUtterance:
    """Source utterance that remains sovereign in the bridge.

    ``source_ref`` and ``source_span`` identify the original source location.
    ``admission_ref`` is required because CA-M019 may only bridge already-admitted
    evidence. ``context_lineage_refs`` must contain at least one parent/context ref
    so that an ExpressionMoment cannot become an orphaned semantic island.
    """

    utterance_id: str
    text: str
    source_ref: Mapping[str, Any]
    source_span: Mapping[str, Any]
    speaker_id: str
    emotional_polarity: str
    subject_stance: str
    admission_ref: Mapping[str, Any]
    context_lineage_refs: tuple[Mapping[str, Any], ...]

    def __post_init__(self) -> None:
        _require_nonempty_string(self.utterance_id, "utterance_id")
        _require_nonempty_string(self.text, "text")
        _require_ref(self.source_ref, "source_ref")
        _require_source_span(self.source_span, "source_span")
        _require_nonempty_string(self.speaker_id, "speaker_id")
        _require_semantic_label(self.emotional_polarity, "emotional_polarity")
        _require_semantic_label(self.subject_stance, "subject_stance")
        _require_ref(self.admission_ref, "admission_ref")
        if self.source_span["source_id"] != self.source_ref["object_id"]:
            raise InvalidBridgeInputError("source_span.source_id must match source_ref.object_id")
        if self.source_span["source_version"] != self.source_ref["version"]:
            raise InvalidBridgeInputError("source_span.source_version must match source_ref.version")
        if self.source_span["source_sha256"] != self.source_ref["sha256"]:
            raise InvalidBridgeInputError("source_span.source_sha256 must match source_ref.sha256")
        if not isinstance(self.context_lineage_refs, tuple) or not self.context_lineage_refs:
            raise InvalidBridgeInputError(
                "context_lineage_refs must contain at least one immutable lineage reference"
            )
        for index, ref in enumerate(self.context_lineage_refs):
            _require_ref(ref, f"context_lineage_refs[{index}]")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "RawSpokenUtterance":
        if not isinstance(value, Mapping):
            raise InvalidBridgeInputError("raw spoken utterance must be a mapping")
        required = {
            "utterance_id",
            "text",
            "source_ref",
            "source_span",
            "speaker_id",
            "emotional_polarity",
            "subject_stance",
            "admission_ref",
            "context_lineage_refs",
        }
        missing = sorted(required.difference(value))
        if missing:
            raise InvalidBridgeInputError(
                "raw spoken utterance is missing required fields",
                context={"missing_fields": missing},
            )
        refs = value["context_lineage_refs"]
        if isinstance(refs, (str, bytes, bytearray)) or not isinstance(refs, Sequence):
            raise InvalidBridgeInputError("context_lineage_refs must be a sequence")
        return cls(
            utterance_id=value["utterance_id"],
            text=value["text"],
            source_ref=value["source_ref"],
            source_span=value["source_span"],
            speaker_id=value["speaker_id"],
            emotional_polarity=value["emotional_polarity"],
            subject_stance=value["subject_stance"],
            admission_ref=value["admission_ref"],
            context_lineage_refs=tuple(refs),
        )


# Friendly alias used by some callers/tests.
RawUtterance = RawSpokenUtterance


@dataclass(frozen=True, slots=True)
class ConceptualActivationVector:
    """High-level semantic vector supplied by an upstream governed classifier.

    The bridge does not derive this vector from free text. Every vector dimension
    is therefore an explicit upstream assertion and is retained verbatim in the
    ExpressionMoment. ``source_utterance_id`` prevents a vector for another
    utterance from being attached accidentally.
    """

    vector_id: str
    source_utterance_id: str
    dimensions: Mapping[str, float]
    emotional_polarity: str
    subject_stance: str
    evidence_refs: tuple[Mapping[str, Any], ...]

    def __post_init__(self) -> None:
        _require_nonempty_string(self.vector_id, "vector_id")
        _require_nonempty_string(self.source_utterance_id, "source_utterance_id")
        if not isinstance(self.dimensions, Mapping) or not self.dimensions:
            raise InvalidBridgeInputError("dimensions must be a non-empty mapping")
        for name, score in self.dimensions.items():
            _require_semantic_label(name, "dimension name")
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not isfinite(score):
                raise InvalidBridgeInputError(
                    f"dimensions[{name!r}] must be a finite numeric activation score"
                )
        _require_semantic_label(self.emotional_polarity, "emotional_polarity")
        _require_semantic_label(self.subject_stance, "subject_stance")
        if not isinstance(self.evidence_refs, tuple) or not self.evidence_refs:
            raise InvalidBridgeInputError("evidence_refs must contain at least one direct evidence ref")
        for index, ref in enumerate(self.evidence_refs):
            _require_ref(ref, f"evidence_refs[{index}]")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ConceptualActivationVector":
        if not isinstance(value, Mapping):
            raise InvalidBridgeInputError("conceptual activation vector must be a mapping")
        required = {
            "vector_id",
            "source_utterance_id",
            "dimensions",
            "emotional_polarity",
            "subject_stance",
            "evidence_refs",
        }
        missing = sorted(required.difference(value))
        if missing:
            raise InvalidBridgeInputError(
                "conceptual activation vector is missing required fields",
                context={"missing_fields": missing},
            )
        refs = value["evidence_refs"]
        if isinstance(refs, (str, bytes, bytearray)) or not isinstance(refs, Sequence):
            raise InvalidBridgeInputError("evidence_refs must be a sequence")
        return cls(
            vector_id=value["vector_id"],
            source_utterance_id=value["source_utterance_id"],
            dimensions=dict(value["dimensions"]),
            emotional_polarity=value["emotional_polarity"],
            subject_stance=value["subject_stance"],
            evidence_refs=tuple(refs),
        )


ActivationVector = ConceptualActivationVector


@dataclass(frozen=True, slots=True)
class ExpressionMoment:
    """Direct semantic bridge record consumed by downstream composition.

    There is intentionally no intermediary-frame field. The moment retains the
    source utterance and the conceptual vector side-by-side, plus immutable source
    and lineage refs. This makes the semantic hop explicit and auditable.
    """

    expression_moment_id: str
    mandate_id: str
    invariant_id: str
    schema_version: str
    source_utterance_id: str
    source_text: str
    source_ref: Mapping[str, Any]
    source_span: Mapping[str, Any]
    speaker_id: str
    admission_ref: Mapping[str, Any]
    context_lineage_refs: tuple[Mapping[str, Any], ...]
    activation_vector: ConceptualActivationVector
    preserved_emotional_polarity: str
    preserved_subject_stance: str
    transformation: str
    intermediary_frames: tuple[Any, ...] = field(default_factory=tuple)
    moment_sha256: str = ""

    def __post_init__(self) -> None:
        if self.mandate_id != MANDATE_ID or self.invariant_id != INVARIANT_ID:
            raise InvalidBridgeInputError("ExpressionMoment authority metadata does not match CA-M019")
        if self.schema_version != SCHEMA_VERSION:
            raise InvalidBridgeInputError("unsupported ExpressionMoment schema version")
        _require_nonempty_string(self.expression_moment_id, "expression_moment_id")
        _require_nonempty_string(self.source_utterance_id, "source_utterance_id")
        _require_nonempty_string(self.source_text, "source_text")
        _require_ref(self.source_ref, "source_ref")
        _require_source_span(self.source_span, "source_span")
        _require_nonempty_string(self.speaker_id, "speaker_id")
        _require_ref(self.admission_ref, "admission_ref")
        if self.source_span["source_id"] != self.source_ref["object_id"]:
            raise InvalidBridgeInputError("source_span.source_id must match source_ref.object_id")
        if self.source_span["source_version"] != self.source_ref["version"]:
            raise InvalidBridgeInputError("source_span.source_version must match source_ref.version")
        if self.source_span["source_sha256"] != self.source_ref["sha256"]:
            raise InvalidBridgeInputError("source_span.source_sha256 must match source_ref.sha256")
        if not isinstance(self.context_lineage_refs, tuple) or not self.context_lineage_refs:
            raise InvalidBridgeInputError("ExpressionMoment requires context lineage")
        for index, ref in enumerate(self.context_lineage_refs):
            _require_ref(ref, f"context_lineage_refs[{index}]")
        if not isinstance(self.activation_vector, ConceptualActivationVector):
            raise InvalidBridgeInputError("activation_vector must be ConceptualActivationVector")
        if self.activation_vector.source_utterance_id != self.source_utterance_id:
            raise SemanticTransformationRejectedError(
                "activation vector is not directly anchored to this utterance",
                context={
                    "utterance_id": self.source_utterance_id,
                    "vector_source_utterance_id": self.activation_vector.source_utterance_id,
                },
            )
        if self.preserved_emotional_polarity != self.activation_vector.emotional_polarity:
            raise SemanticTransformationRejectedError("ExpressionMoment polarity does not match its vector")
        if self.preserved_subject_stance != self.activation_vector.subject_stance:
            raise SemanticTransformationRejectedError("ExpressionMoment stance does not match its vector")
        if self.intermediary_frames:
            raise SemanticTransformationRejectedError(
                "CA-M019 forbids hallucinated intermediary semantic frames",
                context={"intermediary_frames": list(self.intermediary_frames)},
            )
        _require_nonempty_string(self.transformation, "transformation")
        if not self.moment_sha256:
            raise InvalidBridgeInputError("moment_sha256 is required")
        _require_sha256(self.moment_sha256, "moment_sha256")

    def to_dict(self) -> dict[str, Any]:
        return {
            "expression_moment_id": self.expression_moment_id,
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "schema_version": self.schema_version,
            "source_utterance_id": self.source_utterance_id,
            "source_text": self.source_text,
            "source_ref": dict(self.source_ref),
            "source_span": dict(self.source_span),
            "speaker_id": self.speaker_id,
            "admission_ref": dict(self.admission_ref),
            "context_lineage_refs": [dict(ref) for ref in self.context_lineage_refs],
            "activation_vector": {
                "vector_id": self.activation_vector.vector_id,
                "source_utterance_id": self.activation_vector.source_utterance_id,
                "dimensions": dict(self.activation_vector.dimensions),
                "emotional_polarity": self.activation_vector.emotional_polarity,
                "subject_stance": self.activation_vector.subject_stance,
                "evidence_refs": [dict(ref) for ref in self.activation_vector.evidence_refs],
            },
            "preserved_emotional_polarity": self.preserved_emotional_polarity,
            "preserved_subject_stance": self.preserved_subject_stance,
            "transformation": self.transformation,
            "intermediary_frames": list(self.intermediary_frames),
            "moment_sha256": self.moment_sha256,
        }

    def composition_payload(self) -> dict[str, Any]:
        """Return the only supported downstream composition input shape."""

        return self.to_dict()


@dataclass(frozen=True, slots=True)
class SemanticBridgeReceipt:
    """Auditable result of one accepted direct semantic bridge operation."""

    mandate_id: str
    invariant_id: str
    policy_version: str
    expression_moment: ExpressionMoment
    checks: Mapping[str, bool]
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "policy_version": self.policy_version,
            "expression_moment": self.expression_moment.to_dict(),
            "checks": dict(self.checks),
            "receipt_sha256": self.receipt_sha256,
        }


class SemanticBridge:
    """Authoritative CA-M019 direct utterance-to-vector bridge."""

    def bridge(
        self,
        utterance: RawSpokenUtterance | Mapping[str, Any],
        activation_vector: ConceptualActivationVector | Mapping[str, Any],
        *,
        admission_receipt: Any | None = None,
        context_lineage: Any | None = None,
    ) -> SemanticBridgeReceipt:
        source = (
            utterance if isinstance(utterance, RawSpokenUtterance) else RawSpokenUtterance.from_mapping(utterance)
        )
        vector = (
            activation_vector
            if isinstance(activation_vector, ConceptualActivationVector)
            else ConceptualActivationVector.from_mapping(activation_vector)
        )

        self._require_admitted(source, admission_receipt)
        self._require_context_lineage(source, context_lineage)
        self._validate_direct_mapping(source, vector)

        core = {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "schema_version": SCHEMA_VERSION,
            "source_utterance_id": source.utterance_id,
            "source_text": source.text,
            "source_ref": dict(source.source_ref),
            "source_span": dict(source.source_span),
            "speaker_id": source.speaker_id,
            "admission_ref": dict(source.admission_ref),
            "context_lineage_refs": [dict(ref) for ref in source.context_lineage_refs],
            "activation_vector": {
                "vector_id": vector.vector_id,
                "source_utterance_id": vector.source_utterance_id,
                "dimensions": dict(vector.dimensions),
                "emotional_polarity": vector.emotional_polarity,
                "subject_stance": vector.subject_stance,
                "evidence_refs": [dict(ref) for ref in vector.evidence_refs],
            },
            "preserved_emotional_polarity": source.emotional_polarity,
            "preserved_subject_stance": source.subject_stance,
            "transformation": "DIRECT_UTTERANCE_TO_ACTIVATION_VECTOR",
            "intermediary_frames": [],
        }
        moment_sha = _canonical_sha256(core)
        moment = ExpressionMoment(
            expression_moment_id=f"ie:expression-moment:{moment_sha[:32]}",
            mandate_id=MANDATE_ID,
            invariant_id=INVARIANT_ID,
            schema_version=SCHEMA_VERSION,
            source_utterance_id=source.utterance_id,
            source_text=source.text,
            source_ref=dict(source.source_ref),
            source_span=dict(source.source_span),
            speaker_id=source.speaker_id,
            admission_ref=dict(source.admission_ref),
            context_lineage_refs=tuple(dict(ref) for ref in source.context_lineage_refs),
            activation_vector=vector,
            preserved_emotional_polarity=source.emotional_polarity,
            preserved_subject_stance=source.subject_stance,
            transformation="DIRECT_UTTERANCE_TO_ACTIVATION_VECTOR",
            intermediary_frames=(),
            moment_sha256=moment_sha,
        )
        receipt_core = {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "policy_version": POLICY_VERSION,
            "expression_moment": moment.to_dict(),
            "checks": {
                "admitted_evidence": True,
                "context_lineage_present": True,
                "direct_utterance_anchor": True,
                "polarity_preserved": True,
                "subject_stance_preserved": True,
                "no_intermediary_frames": True,
            },
        }
        receipt_sha = _canonical_sha256(receipt_core)
        return SemanticBridgeReceipt(
            mandate_id=MANDATE_ID,
            invariant_id=INVARIANT_ID,
            policy_version=POLICY_VERSION,
            expression_moment=moment,
            checks=receipt_core["checks"],
            receipt_sha256=receipt_sha,
        )

    def transform(
        self,
        utterance: RawSpokenUtterance | Mapping[str, Any],
        activation_vector: ConceptualActivationVector | Mapping[str, Any],
        *,
        admission_receipt: Any | None = None,
        context_lineage: Any | None = None,
    ) -> SemanticBridgeReceipt:
        """Alias for callers that name the semantic operation ``transform``."""

        return self.bridge(
            utterance,
            activation_vector,
            admission_receipt=admission_receipt,
            context_lineage=context_lineage,
        )

    def build_expression_moment(
        self,
        utterance: RawSpokenUtterance | Mapping[str, Any],
        activation_vector: ConceptualActivationVector | Mapping[str, Any],
        *,
        admission_receipt: Any | None = None,
        context_lineage: Any | None = None,
    ) -> ExpressionMoment:
        """Return the bridged ExpressionMoment after all CA-M019 gates pass."""

        return self.bridge(
            utterance,
            activation_vector,
            admission_receipt=admission_receipt,
            context_lineage=context_lineage,
        ).expression_moment

    def require_composition_input(self, value: Any) -> ExpressionMoment:
        """Fail closed unless the caller supplies a genuine ExpressionMoment.

        A mapping is not accepted merely because it has an ``expression_moment``
        looking field. This prevents a false-proof object from becoming a semantic
        bypass at a composition boundary.
        """

        if not isinstance(value, ExpressionMoment):
            raise RawCompositionInputRejectedError(
                "composition requires an ExpressionMoment produced by SemanticBridge.bridge",
                context={"received_type": type(value).__name__},
            )
        if value.mandate_id != MANDATE_ID or value.invariant_id != INVARIANT_ID:
            raise RawCompositionInputRejectedError("composition input carries incompatible semantic authority")
        if value.intermediary_frames:
            raise RawCompositionInputRejectedError("composition input contains forbidden intermediary frames")
        return value

    def _require_admitted(self, utterance: RawSpokenUtterance, admission_receipt: Any | None) -> None:
        if admission_receipt is None:
            # The source carries an admission ref, but CA-M019 must not infer that
            # a reference alone means admission. The caller must bring the actual
            # authoritative receipt when the bridge is invoked.
            raise InvalidBridgeInputError(
                "CA-M019 requires the authoritative admission receipt; an admission ref alone is not enough"
            )

        if not _receipt_admitted(admission_receipt):
            raise SemanticTransformationRejectedError(
                "semantic bridge input is not admitted evidence",
                context={"reason_code": "EVIDENCE_NOT_ADMITTED"},
            )
        if _receipt_generation_blocked(admission_receipt):
            raise SemanticTransformationRejectedError(
                "semantic bridge input is barred downstream by its admission receipt",
                context={"reason_code": "DOWNSTREAM_GENERATION_BLOCKED"},
            )
        receipt_id = _read_ref_id(utterance.admission_ref)
        actual_id = _receipt_evidence_id(admission_receipt)
        if actual_id is not None and receipt_id != actual_id:
            raise SemanticTransformationRejectedError(
                "utterance admission ref does not match the authoritative admission receipt",
                context={"admission_ref": receipt_id, "receipt_evidence_id": actual_id},
            )

    def _require_context_lineage(self, utterance: RawSpokenUtterance, context_lineage: Any | None) -> None:
        if context_lineage is None:
            raise InvalidBridgeInputError(
                "CA-M019 requires the authoritative context-lineage result; local refs alone are not sufficient"
            )
        if not _lineage_valid(context_lineage):
            raise SemanticTransformationRejectedError(
                "semantic bridge input lacks valid hierarchical context lineage",
                context={"reason_code": "CONTEXT_LINEAGE_INVALID"},
            )
        lineage_ids = {_read_ref_id(ref) for ref in utterance.context_lineage_refs}
        observed_ids = _lineage_ids(context_lineage)
        if observed_ids and not lineage_ids.intersection(observed_ids):
            raise SemanticTransformationRejectedError(
                "utterance lineage refs do not intersect authoritative context lineage",
                context={
                    "utterance_lineage_refs": sorted(lineage_ids),
                    "authoritative_lineage_refs": sorted(observed_ids),
                },
            )

    @staticmethod
    def _validate_direct_mapping(
        utterance: RawSpokenUtterance,
        vector: ConceptualActivationVector,
    ) -> None:
        if vector.source_utterance_id != utterance.utterance_id:
            raise SemanticTransformationRejectedError(
                "conceptual activation vector must identify the exact source utterance",
                context={
                    "utterance_id": utterance.utterance_id,
                    "vector_source_utterance_id": vector.source_utterance_id,
                },
            )
        if vector.emotional_polarity != utterance.emotional_polarity:
            raise SemanticTransformationRejectedError(
                "semantic transformation changes core emotional polarity",
                context={
                    "source_emotional_polarity": utterance.emotional_polarity,
                    "vector_emotional_polarity": vector.emotional_polarity,
                },
            )
        if vector.subject_stance != utterance.subject_stance:
            raise SemanticTransformationRejectedError(
                "semantic transformation changes subject stance",
                context={
                    "source_subject_stance": utterance.subject_stance,
                    "vector_subject_stance": vector.subject_stance,
                },
            )
        if not vector.evidence_refs:
            raise SemanticTransformationRejectedError("activation vector has no direct evidence anchors")


def bridge_expression_moment(
    utterance: RawSpokenUtterance | Mapping[str, Any],
    activation_vector: ConceptualActivationVector | Mapping[str, Any],
    *,
    admission_receipt: Any | None = None,
    context_lineage: Any | None = None,
) -> SemanticBridgeReceipt:
    """Convenience entry point for the CA-M019 authoritative bridge."""

    return SemanticBridge().bridge(
        utterance,
        activation_vector,
        admission_receipt=admission_receipt,
        context_lineage=context_lineage,
    )


def require_expression_moment(value: Any) -> ExpressionMoment:
    """Convenience composition guard."""

    return SemanticBridge().require_composition_input(value)


def _receipt_admitted(receipt: Any) -> bool:
    value = _read_attr_or_key(receipt, "admitted")
    return value is True


def _receipt_generation_blocked(receipt: Any) -> bool:
    value = _read_attr_or_key(receipt, "downstream_generation_allowed", default=True)
    return value is False


def _receipt_evidence_id(receipt: Any) -> str | None:
    value = _read_attr_or_key(receipt, "evidence_id", default=None)
    return value if isinstance(value, str) and value.strip() else None


def _lineage_valid(lineage: Any) -> bool:
    for key in ("valid", "admitted", "is_valid", "cycle_free"):
        value = _read_attr_or_key(lineage, key, default=None)
        if value is False:
            return False
    return True


def _lineage_ids(lineage: Any) -> set[str]:
    ids: set[str] = set()
    candidates = _read_attr_or_key(lineage, "node_refs", default=None)
    if candidates is None:
        candidates = _read_attr_or_key(lineage, "lineage_refs", default=None)
    if candidates is None and isinstance(lineage, Mapping):
        candidates = lineage.get("refs")
    if isinstance(candidates, Sequence) and not isinstance(candidates, (str, bytes, bytearray)):
        for item in candidates:
            if isinstance(item, Mapping):
                try:
                    ids.add(_read_ref_id(item))
                except InvalidBridgeInputError:
                    continue
    else:
        direct = _read_attr_or_key(lineage, "node_id", default=None)
        if isinstance(direct, str) and direct.strip():
            ids.add(direct.strip())
    return ids


def _read_attr_or_key(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(key, default)
    return getattr(value, key, default)


def _read_ref_id(value: Mapping[str, Any]) -> str:
    _require_ref(value, "ref")
    return str(value["object_id"])


def _require_ref(value: Any, name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise InvalidBridgeInputError(f"{name} must be a mapping")
    required = {"object_id", "version", "sha256"}
    if set(value) != required:
        raise InvalidBridgeInputError(
            f"{name} fields mismatch",
            context={"required": sorted(required), "observed": sorted(value)},
        )
    object_id = _require_nonempty_string(value["object_id"], f"{name}.object_id")
    version = _require_nonempty_string(value["version"], f"{name}.version")
    sha = _require_sha256(value["sha256"], f"{name}.sha256")
    return {"object_id": object_id, "version": version, "sha256": sha}


def _require_source_span(value: Any, name: str = "source_span") -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise InvalidBridgeInputError(f"{name} must be a mapping")
    required = {"source_id", "source_version", "source_sha256", "start_ms", "end_ms", "speaker_id"}
    if set(value) != required:
        raise InvalidBridgeInputError(
            f"{name} fields mismatch",
            context={"required": sorted(required), "observed": sorted(value)},
        )
    start = value["start_ms"]
    end = value["end_ms"]
    if isinstance(start, bool) or not isinstance(start, int) or start < 0:
        raise InvalidBridgeInputError(f"{name}.start_ms must be a non-negative integer")
    if isinstance(end, bool) or not isinstance(end, int) or end <= start:
        raise InvalidBridgeInputError(f"{name}.end_ms must be an integer greater than start_ms")
    _require_nonempty_string(value["source_id"], f"{name}.source_id")
    _require_nonempty_string(value["source_version"], f"{name}.source_version")
    _require_sha256(value["source_sha256"], f"{name}.source_sha256")
    _require_nonempty_string(value["speaker_id"], f"{name}.speaker_id")
    return dict(value)


def _require_semantic_label(value: Any, name: str) -> str:
    return _require_nonempty_string(value, name)


def _require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidBridgeInputError(f"{name} must be a non-empty string")
    return value.strip()


def _require_sha256(value: Any, name: str) -> str:
    text = _require_nonempty_string(value, name)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise InvalidBridgeInputError(f"{name} must be a lowercase SHA-256")
    return text


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


__all__ = [
    "MANDATE_ID",
    "INVARIANT_ID",
    "SCHEMA_VERSION",
    "POLICY_VERSION",
    "EmotionalPolarity",
    "RawSpokenUtterance",
    "RawUtterance",
    "ConceptualActivationVector",
    "ActivationVector",
    "ExpressionMoment",
    "SemanticBridgeReceipt",
    "SemanticBridge",
    "SemanticBridgeError",
    "InvalidBridgeInputError",
    "SemanticTransformationRejectedError",
    "RawCompositionInputRejectedError",
    "bridge_expression_moment",
    "require_expression_moment",
]
