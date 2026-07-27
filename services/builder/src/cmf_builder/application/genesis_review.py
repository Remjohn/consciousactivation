"""Genesis decision and authority review projection for OD-AM-003 / ST-10.04."""

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


class GenesisReviewError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class DecisionClass(str, Enum):
    CONSTITUTIONAL = "CONSTITUTIONAL"
    PRODUCT_BOUNDARY = "PRODUCT_BOUNDARY"
    ATOMIC_BOUNDARY = "ATOMIC_BOUNDARY"
    CATEGORY = "CATEGORY"
    IDENTITY = "IDENTITY"
    HUMAN_AUTHORITY = "HUMAN_AUTHORITY"
    EVIDENCE_ADMISSION = "EVIDENCE_ADMISSION"
    MATURITY = "MATURITY"
    WORKFLOW_POLICY = "WORKFLOW_POLICY"
    EXTERNAL_HANDOFF = "EXTERNAL_HANDOFF"
    CERTIFICATION_POLICY = "CERTIFICATION_POLICY"


class OwnerType(str, Enum):
    HUMAN = "HUMAN"
    GOVERNED_OPERATOR = "GOVERNED_OPERATOR"
    CONSTITUTION = "CONSTITUTION"
    BUILDER_RULE = "BUILDER_RULE"
    DETERMINISTIC_CODE = "DETERMINISTIC_CODE"
    AGENT_PROPOSAL = "AGENT_PROPOSAL"
    EXTERNAL_AUTHORITY = "EXTERNAL_AUTHORITY"


class DecisionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"
    PROPOSED = "PROPOSED"
    EXPIRED = "EXPIRED"


class ReviewDisposition(str, Enum):
    VALID_ACTIVE = "VALID_ACTIVE"
    VALID_LIMITED_SCOPE = "VALID_LIMITED_SCOPE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"
    MISSING_AUTHORITY = "MISSING_AUTHORITY"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    CONFLICTING_AUTHORITY = "CONFLICTING_AUTHORITY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    PROPOSAL_ONLY = "PROPOSAL_ONLY"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GenesisReviewError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class GenesisDecision:
    decision_identity: str
    decision_class: DecisionClass
    subject_identity: str
    originating_context: str
    decision_owner: str
    owner_type: OwnerType
    authority_basis: str
    effective_date: str
    status: DecisionStatus
    decision_statement: str
    supporting_evidence: tuple[str, ...]
    conflicting_evidence: tuple[str, ...]
    limitations: tuple[str, ...]
    scope: tuple[str, ...]
    excluded_scope: tuple[str, ...]
    predecessor_decisions: tuple[str, ...]
    superseding_decisions: tuple[str, ...]
    dependent_objects: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    review_state: str
    redacted_fields: tuple[str, ...] = ()
    production_authority: bool = False
    certified_authority: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.decision_identity, "decision_identity"),
            (self.subject_identity, "subject_identity"),
            (self.originating_context, "originating_context"),
            (self.decision_owner, "decision_owner"),
            (self.authority_basis, "authority_basis"),
            (self.effective_date, "effective_date"),
            (self.decision_statement, "decision_statement"),
            (self.review_state, "review_state"),
        ):
            _text(value, name)
        if self.owner_type is OwnerType.AGENT_PROPOSAL and self.status is DecisionStatus.ACTIVE:
            raise GenesisReviewError("AGENT_PROPOSAL_NOT_APPROVAL", "agent proposals cannot be active human or operator decisions")
        if self.owner_type is OwnerType.DETERMINISTIC_CODE and self.decision_class in {DecisionClass.HUMAN_AUTHORITY, DecisionClass.CERTIFICATION_POLICY}:
            raise GenesisReviewError("DETERMINISTIC_CODE_NOT_POLICY_AUTHORITY", "deterministic code cannot own human or certification authority")
        if self.production_authority and "production" not in self.scope:
            raise GenesisReviewError("PRODUCTION_SCOPE_NOT_GOVERNED", "production authority requires explicit scope")
        if self.certified_authority and self.decision_class is not DecisionClass.CERTIFICATION_POLICY:
            raise GenesisReviewError("CERTIFICATION_CLASS_REQUIRED", "certification authority requires certification policy class")

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision_identity": self.decision_identity,
            "decision_class": self.decision_class.value,
            "subject_identity": self.subject_identity,
            "originating_context": self.originating_context,
            "decision_owner": self.decision_owner,
            "owner_type": self.owner_type.value,
            "authority_basis": self.authority_basis,
            "effective_date": self.effective_date,
            "status": self.status.value,
            "decision_statement": self.decision_statement,
            "supporting_evidence": list(self.supporting_evidence),
            "conflicting_evidence": list(self.conflicting_evidence),
            "limitations": list(self.limitations),
            "scope": list(self.scope),
            "excluded_scope": list(self.excluded_scope),
            "predecessor_decisions": list(self.predecessor_decisions),
            "superseding_decisions": list(self.superseding_decisions),
            "dependent_objects": list(self.dependent_objects),
            "invalidation_conditions": list(self.invalidation_conditions),
            "review_state": self.review_state,
            "redacted_fields": list(self.redacted_fields),
            "production_authority": self.production_authority,
            "certified_authority": self.certified_authority,
        }


@dataclass(frozen=True)
class GenesisReviewResult:
    decision_identity: str
    disposition: ReviewDisposition
    reason: str
    dependent_objects: tuple[str, ...]
    redacted_fields: tuple[str, ...]
    underlying_decision_mutated: bool = False
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _text(self.decision_identity, "decision_identity")
        _text(self.reason, "reason")
        if self.underlying_decision_mutated:
            raise GenesisReviewError("REVIEW_CANNOT_AMEND_DECISION", "review projections cannot amend decisions")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "decision_identity": self.decision_identity,
            "disposition": self.disposition.value,
            "reason": self.reason,
            "dependent_objects": list(self.dependent_objects),
            "redacted_fields": list(self.redacted_fields),
            "underlying_decision_mutated": False,
        }

    @property
    def review_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise GenesisReviewError("MUTATED_GOVERNED_OBJECT", "review result changed")
        payload["review_identity"] = sha256_of(payload)
        return payload


def review_genesis_decision(decision: GenesisDecision, *, requested_scope: str = "development") -> GenesisReviewResult:
    if decision.status is DecisionStatus.PROPOSED:
        disposition = ReviewDisposition.PROPOSAL_ONLY
        reason = "proposal is not a governed approval"
    elif decision.status is DecisionStatus.SUPERSEDED:
        disposition = ReviewDisposition.SUPERSEDED
        reason = "decision has a superseding decision"
    elif decision.status is DecisionStatus.INVALIDATED:
        disposition = ReviewDisposition.INVALIDATED
        reason = "decision has been invalidated"
    elif decision.status is DecisionStatus.EXPIRED:
        disposition = ReviewDisposition.MISSING_AUTHORITY
        reason = "approval expired or is no longer active"
    elif not decision.authority_basis:
        disposition = ReviewDisposition.MISSING_AUTHORITY
        reason = "missing authority basis"
    elif not decision.supporting_evidence:
        disposition = ReviewDisposition.MISSING_EVIDENCE
        reason = "missing supporting evidence"
    elif decision.conflicting_evidence:
        disposition = ReviewDisposition.CONFLICTING_AUTHORITY
        reason = "conflicting evidence or authority is recorded"
    elif requested_scope not in decision.scope:
        disposition = ReviewDisposition.VALID_LIMITED_SCOPE
        reason = "decision is valid but does not cover requested scope"
    else:
        disposition = ReviewDisposition.VALID_ACTIVE
        reason = "decision is active for requested scope"
    return GenesisReviewResult(decision.decision_identity, disposition, reason, decision.dependent_objects, decision.redacted_fields)


def filter_decisions(
    decisions: tuple[GenesisDecision, ...],
    *,
    subject_identity: str | None = None,
    owner: str | None = None,
    decision_class: DecisionClass | None = None,
    status: DecisionStatus | None = None,
) -> tuple[GenesisDecision, ...]:
    result = []
    for decision in decisions:
        if subject_identity is not None and decision.subject_identity != subject_identity:
            continue
        if owner is not None and decision.decision_owner != owner:
            continue
        if decision_class is not None and decision.decision_class is not decision_class:
            continue
        if status is not None and decision.status is not status:
            continue
        result.append(decision)
    return tuple(sorted(result, key=lambda item: item.decision_identity))
