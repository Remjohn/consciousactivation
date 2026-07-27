"""Evidence and syntax inspection projections for OD-AM-003 / ST-10.03."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class DecisionInspectionError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class SubjectType(str, Enum):
    DECISION = "DECISION"
    RUN = "RUN"
    HARNESS = "HARNESS"
    WORKFLOW = "WORKFLOW"
    STORY = "STORY"
    OBLIGATION = "OBLIGATION"
    RECEIPT = "RECEIPT"
    PHASE = "PHASE"
    GRAPH_NODE = "GRAPH_NODE"
    SYNTAX = "SYNTAX"


class EvidenceKind(str, Enum):
    RAW_SOURCE_REFERENCE = "RAW_SOURCE_REFERENCE"
    NORMALIZED_OBSERVATION = "NORMALIZED_OBSERVATION"
    SYNTAX_RELATIONSHIP = "SYNTAX_RELATIONSHIP"
    PROVISIONAL_GRAMMAR = "PROVISIONAL_GRAMMAR"
    CATEGORY_PROFILE = "CATEGORY_PROFILE"
    ACTIVATIVE_SEQUENCE = "ACTIVATIVE_SEQUENCE"
    WRONG_READING_LOCK = "WRONG_READING_LOCK"
    AUTHORITY_RECORD = "AUTHORITY_RECORD"
    DECISION_RECORD = "DECISION_RECORD"
    EVALUATION_RESULT = "EVALUATION_RESULT"
    REPAIR_RESULT = "REPAIR_RESULT"


class EvidenceState(str, Enum):
    ACTIVE_SUPPORTING = "ACTIVE_SUPPORTING"
    ACTIVE_CONFLICTING = "ACTIVE_CONFLICTING"
    EXCLUDED = "EXCLUDED"
    INVALIDATED = "INVALIDATED"
    REDACTED = "REDACTED"
    MISSING = "MISSING"
    STALE = "STALE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SyntaxKind(str, Enum):
    SPATIAL_RELATIONSHIP = "spatial_relationship"
    TEMPORAL_RELATIONSHIP = "temporal_relationship"
    READING_ORDER = "reading_order"
    CONVERSATIONAL_ORDER = "conversational_order"
    CHARACTER_PERFORMANCE_GRAMMAR = "character_performance_grammar"
    CATEGORY_NATIVE_SYNTAX = "category_native_syntax"
    PROVISIONAL_GRAMMAR = "provisional_grammar"
    ACTIVATIVE_SEQUENCING = "activative_sequencing"
    WRONG_READING_LOCK = "wrong_reading_lock"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DecisionInspectionError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str
    kind: EvidenceKind
    state: EvidenceState
    source_provenance: str
    lineage_ref: str
    redaction_basis: str = ""
    limitation: str = ""

    def __post_init__(self) -> None:
        for value, name in (
            (self.evidence_id, "evidence_id"),
            (self.source_provenance, "source_provenance"),
            (self.lineage_ref, "lineage_ref"),
        ):
            _text(value, name)
        if self.state is EvidenceState.REDACTED and not self.redaction_basis:
            raise DecisionInspectionError("REDACTION_BASIS_REQUIRED", "redacted evidence requires basis")
        if self.state is EvidenceState.NOT_APPLICABLE and "NOT_APPLICABLE" not in self.limitation:
            raise DecisionInspectionError("NOT_APPLICABLE_BASIS_REQUIRED", "not-applicable evidence requires basis")

    @property
    def evidence_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "kind": self.kind.value,
            "state": self.state.value,
            "source_provenance": self.source_provenance,
            "lineage_ref": self.lineage_ref,
            "redaction_basis": self.redaction_basis,
            "limitation": self.limitation,
        }


@dataclass(frozen=True)
class SyntaxObservation:
    syntax_id: str
    syntax_kind: SyntaxKind
    source_lineage: str
    canonical_compiled_ref: str
    observation: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.syntax_id, "syntax_id"),
            (self.source_lineage, "source_lineage"),
            (self.canonical_compiled_ref, "canonical_compiled_ref"),
            (self.observation, "observation"),
        ):
            _text(value, name)

    def as_dict(self) -> dict[str, Any]:
        return {
            "syntax_id": self.syntax_id,
            "syntax_kind": self.syntax_kind.value,
            "source_lineage": self.source_lineage,
            "canonical_compiled_ref": self.canonical_compiled_ref,
            "observation": self.observation,
        }


@dataclass(frozen=True)
class DecisionInspectionResult:
    inspected_subject: str
    subject_type: SubjectType
    governing_decision: str
    decision_status: str
    authority_owner: str
    evidence: tuple[EvidenceReference, ...]
    syntax_observations: tuple[SyntaxObservation, ...]
    predecessor_decisions: tuple[str, ...]
    superseding_decisions: tuple[str, ...]
    downstream_dependencies: tuple[str, ...]
    uncertainty: str
    knowledge_status: str
    limitations: tuple[str, ...]
    projection_freshness: str
    production_ready: bool = False
    certified: bool = False
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for value, name in (
            (self.inspected_subject, "inspected_subject"),
            (self.governing_decision, "governing_decision"),
            (self.decision_status, "decision_status"),
            (self.authority_owner, "authority_owner"),
            (self.uncertainty, "uncertainty"),
            (self.knowledge_status, "knowledge_status"),
            (self.projection_freshness, "projection_freshness"),
        ):
            _text(value, name)
        if self.production_ready or self.certified:
            raise DecisionInspectionError("FALSE_PRODUCTION_OR_CERTIFICATION_DISPLAY", "inspection cannot display development status as certification")
        states = {item.state for item in self.evidence}
        if not self.evidence:
            raise DecisionInspectionError("MISSING_TRACEABLE_EVIDENCE", "inspection requires immutable evidence references")
        if EvidenceState.ACTIVE_CONFLICTING in states and "conflict" not in " ".join(self.limitations).lower():
            raise DecisionInspectionError("CONFLICTING_EVIDENCE_MUST_BE_VISIBLE", "conflicting evidence must be disclosed")
        if any(item.kind is EvidenceKind.AUTHORITY_RECORD for item in self.evidence) is False:
            raise DecisionInspectionError("AUTHORITY_RECORD_REQUIRED", "inspection requires authority trace")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "inspected_subject": self.inspected_subject,
            "subject_type": self.subject_type.value,
            "governing_decision": self.governing_decision,
            "decision_status": self.decision_status,
            "authority_owner": self.authority_owner,
            "evidence": [item.as_dict() for item in sorted(self.evidence, key=lambda item: item.evidence_id)],
            "syntax_observations": [item.as_dict() for item in sorted(self.syntax_observations, key=lambda item: item.syntax_id)],
            "predecessor_decisions": list(self.predecessor_decisions),
            "superseding_decisions": list(self.superseding_decisions),
            "downstream_dependencies": list(self.downstream_dependencies),
            "uncertainty": self.uncertainty,
            "knowledge_status": self.knowledge_status,
            "limitations": list(self.limitations),
            "projection_freshness": self.projection_freshness,
            "production_ready": False,
            "certified": False,
        }

    @property
    def inspection_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise DecisionInspectionError("MUTATED_GOVERNED_OBJECT", "inspection projection changed")
        payload["inspection_identity"] = sha256_of(payload)
        return payload


def structured_explanation(result: DecisionInspectionResult) -> dict[str, Any]:
    states = {state.value: [] for state in EvidenceState}
    for item in result.evidence:
        states[item.state.value].append(item.evidence_id)
    return {
        "what_was_decided": result.governing_decision,
        "who_or_what_owned_the_decision": result.authority_owner,
        "supporting_evidence": states[EvidenceState.ACTIVE_SUPPORTING.value],
        "conflicting_evidence": states[EvidenceState.ACTIVE_CONFLICTING.value],
        "excluded_evidence": states[EvidenceState.EXCLUDED.value],
        "invalidated_evidence": states[EvidenceState.INVALIDATED.value],
        "redacted_evidence": states[EvidenceState.REDACTED.value],
        "missing_evidence": states[EvidenceState.MISSING.value],
        "uncertainty_remaining": result.uncertainty,
        "downstream_objects": list(result.downstream_dependencies),
        "superseded_or_invalidated": bool(result.superseding_decisions or result.decision_status in {"SUPERSEDED", "INVALIDATED"}),
        "inspection_is_authoritative_source": False,
    }
