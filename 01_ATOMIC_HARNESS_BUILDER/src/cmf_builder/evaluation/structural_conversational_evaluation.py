"""Structural, synthetic, non-personal conversational evaluation for ST-08.07."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re
from typing import Any

CONVERSATIONAL_DIMENSION_IDS = (
    "role_clarity", "pattern_match", "pattern_interruption", "prediction",
    "payoff", "affinity", "anticipation", "residue", "anti_cliche",
    "no_text_survival", "wrong_reading_rejection",
)
ALLOWED_PROFILES = ("public_comment", "reply_dm", "reelcast_expression", "interview_expression")
_SHA = re.compile(r"^[0-9a-f]{64}$")


class EvaluationError(ValueError):
    def __init__(self, code: str, message: str, **context: object):
        super().__init__(message)
        self.code = code
        self.context = dict(context)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _sha(value: object, name: str) -> None:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        raise EvaluationError("INVALID_IMMUTABLE_IDENTITY", f"{name} must be SHA-256")


class EvaluationDecision(str, Enum):
    PASS_STRUCTURAL_DEVELOPMENT_ONLY = "PASS_STRUCTURAL_DEVELOPMENT_ONLY"
    FAIL_WRONG_READING_LOCK = "FAIL_WRONG_READING_LOCK"
    FAIL_STRUCTURAL_DIMENSION = "FAIL_STRUCTURAL_DIMENSION"
    BLOCKED_HUMAN_EVIDENCE_REQUIRED = "BLOCKED_HUMAN_EVIDENCE_REQUIRED"
    BLOCKED_AUTHORITY = "BLOCKED_AUTHORITY"


StructuralDecision = EvaluationDecision


class ApplicabilityState(str, Enum):
    STRUCTURALLY_APPLICABLE_HUMAN_EVIDENCE_NOT_PROVIDED = "STRUCTURALLY_APPLICABLE_HUMAN_EVIDENCE_NOT_PROVIDED"
    NOT_APPLICABLE_WITH_JUSTIFICATION = "NOT_APPLICABLE_WITH_JUSTIFICATION"


class ConsentState(str, Enum):
    EXPLICIT_SYNTHETIC_NO_HUMAN_EVIDENCE = "EXPLICIT_SYNTHETIC_NO_HUMAN_EVIDENCE"
    WITHDRAWN = "WITHDRAWN"


class DimensionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class GovernedEvidenceRef:
    ref_id: str
    version: str
    sha256: str
    authority_ref: str

    def __post_init__(self) -> None:
        _text(self.ref_id, "ref_id")
        _text(self.version, "version")
        _sha(self.sha256, "sha256")
        _sha(self.authority_ref, "authority_ref")

    def as_dict(self) -> dict[str, str]:
        return {"ref_id": self.ref_id, "version": self.version, "sha256": self.sha256, "authority_ref": self.authority_ref}


@dataclass(frozen=True)
class WrongReadingLock:
    lock_id: str
    prohibited_reading: str
    protected_meaning_ref: GovernedEvidenceRef
    source_and_authority_refs: tuple[GovernedEvidenceRef, ...]
    applicability: str
    rejection_rule: str
    dominant: bool

    def __post_init__(self) -> None:
        _text(self.lock_id, "lock_id")
        _text(self.prohibited_reading, "prohibited_reading")
        _text(self.applicability, "applicability")
        _text(self.rejection_rule, "rejection_rule")
        if not self.source_and_authority_refs:
            raise EvaluationError("MISSING_GOVERNED_FIELD", "source_and_authority_refs are required")

    def as_dict(self) -> dict[str, Any]:
        return {"lock_id": self.lock_id, "prohibited_reading": self.prohibited_reading, "protected_meaning_ref": self.protected_meaning_ref.as_dict(), "source_and_authority_refs": [item.as_dict() for item in self.source_and_authority_refs], "applicability": self.applicability, "rejection_rule": self.rejection_rule, "dominant": self.dominant}


@dataclass(frozen=True)
class IndependentDimensionResult:
    dimension_id: str
    status: DimensionStatus
    evidence_refs: tuple[GovernedEvidenceRef, ...]
    limitation: str
    failure_context: str
    not_applicable_basis: GovernedEvidenceRef | None = None

    def __post_init__(self) -> None:
        _text(self.dimension_id, "dimension_id")
        if self.dimension_id not in CONVERSATIONAL_DIMENSION_IDS:
            raise EvaluationError("UNKNOWN_CONVERSATIONAL_DIMENSION", "unknown dimension")
        if not self.evidence_refs:
            raise EvaluationError("MISSING_DIMENSION_EVIDENCE", "dimension evidence is required")
        _text(self.limitation, "limitation")
        if self.status is DimensionStatus.NOT_APPLICABLE and self.not_applicable_basis is None:
            raise EvaluationError("MISSING_NOT_APPLICABLE_BASIS", "NOT_APPLICABLE requires authority basis")

    def as_dict(self) -> dict[str, Any]:
        return {"dimension_id": self.dimension_id, "status": self.status.value, "evidence_refs": [item.as_dict() for item in self.evidence_refs], "limitation": self.limitation, "failure_context": self.failure_context, "not_applicable_basis": None if self.not_applicable_basis is None else self.not_applicable_basis.as_dict()}


DimensionResult = IndependentDimensionResult


@dataclass(frozen=True)
class HumanOwnedArtifactApplicability:
    artifact_kind: str
    state: ApplicabilityState
    justification: str

    def __post_init__(self) -> None:
        _text(self.artifact_kind, "artifact_kind")
        _text(self.justification, "justification")

    def as_dict(self) -> dict[str, str]:
        return {"artifact_kind": self.artifact_kind, "state": self.state.value, "justification": self.justification}


@dataclass(frozen=True)
class StructuralFixtureClassification:
    repository_owned: bool = True
    synthetic: bool = True
    structural_only: bool = True
    non_personal: bool = True
    non_production: bool = True
    uncertified: bool = True

    def as_dict(self) -> dict[str, bool]:
        return {"repository_owned": self.repository_owned, "synthetic": self.synthetic, "structural_only": self.structural_only, "non_personal": self.non_personal, "non_production": self.non_production, "uncertified": self.uncertified}


@dataclass(frozen=True)
class StructuralEvaluationSubject:
    subject_id: str
    subject_version: str
    subject_sha256: str
    fixture_id: str
    fixture_sha256: str
    category_id: str
    profile_id: str
    expected_reading: str
    proposed_reading: str
    response_ownership: str
    consent_state: ConsentState | str
    evidence_active: bool
    semantic_lineage_refs: tuple[GovernedEvidenceRef, ...]
    authority_refs: tuple[GovernedEvidenceRef, ...]
    production_ready: bool = False
    certified: bool = False
    fixture_classification: StructuralFixtureClassification = field(default_factory=StructuralFixtureClassification)

    def __post_init__(self) -> None:
        for value, name in ((self.subject_id, "subject_id"), (self.subject_version, "subject_version"), (self.fixture_id, "fixture_id"), (self.category_id, "category_id"), (self.profile_id, "profile_id"), (self.expected_reading, "expected_reading"), (self.proposed_reading, "proposed_reading"), (self.response_ownership, "response_ownership")):
            _text(value, name)
        _sha(self.subject_sha256, "subject_sha256")
        _sha(self.fixture_sha256, "fixture_sha256")
        if self.category_id != "conversational_activation_expression" or self.profile_id not in ALLOWED_PROFILES:
            raise EvaluationError("UNSUPPORTED_CONVERSATIONAL_PROFILE", "category/profile is outside the structural branch")
        if not self.semantic_lineage_refs:
            raise EvaluationError("MISSING_SEMANTIC_LINEAGE", "semantic lineage required")
        if not self.authority_refs:
            raise EvaluationError("MISSING_AUTHORITY", "authority references required")
        if self.production_ready or self.certified:
            raise EvaluationError("PRODUCTION_OR_CERTIFICATION_PROHIBITED", "structural branch cannot promote status")
        if not all(self.fixture_classification.as_dict().values()):
            raise EvaluationError("INVALID_STRUCTURAL_FIXTURE_CLASSIFICATION", "all bounded fixture flags must be true")

    @property
    def subject_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        consent = self.consent_state.value if isinstance(self.consent_state, ConsentState) else self.consent_state
        return {"subject_id": self.subject_id, "subject_version": self.subject_version, "subject_sha256": self.subject_sha256, "fixture_id": self.fixture_id, "fixture_sha256": self.fixture_sha256, "category_id": self.category_id, "profile_id": self.profile_id, "expected_reading": self.expected_reading, "proposed_reading": self.proposed_reading, "response_ownership": self.response_ownership, "consent_state": consent, "evidence_active": self.evidence_active, "semantic_lineage_refs": [item.as_dict() for item in self.semantic_lineage_refs], "authority_refs": [item.as_dict() for item in self.authority_refs], "fixture_classification": self.fixture_classification.as_dict(), "production_ready": False, "certified": False}


@dataclass(frozen=True)
class WrongReadingLockResult:
    lock_id: str
    matched: bool
    protected_meaning_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {"lock_id": self.lock_id, "matched": self.matched, "protected_meaning_ref": self.protected_meaning_ref}


@dataclass(frozen=True)
class StructuralConversationalEvaluationReceipt:
    subject: StructuralEvaluationSubject
    decision: EvaluationDecision
    wrong_reading_lock_results: tuple[WrongReadingLockResult, ...]
    independent_dimension_results: tuple[IndependentDimensionResult, ...]
    human_owned_artifacts: tuple[HumanOwnedArtifactApplicability, ...]
    predecessor_receipts: tuple[str, ...]
    active: bool
    historical_reproduction_preserved: bool = True
    production_ready: bool = False
    certified: bool = False
    _integrity_anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for item in self.predecessor_receipts:
            _sha(item, "predecessor_receipt")
        object.__setattr__(self, "_integrity_anchor", canonical_sha256(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {"subject": self.subject.as_dict(), "decision": self.decision.value, "wrong_reading_lock_results": [item.as_dict() for item in self.wrong_reading_lock_results], "independent_dimension_results": [item.as_dict() for item in sorted(self.independent_dimension_results, key=lambda item: CONVERSATIONAL_DIMENSION_IDS.index(item.dimension_id))], "human_owned_artifacts": [item.as_dict() for item in sorted(self.human_owned_artifacts, key=lambda item: item.artifact_kind)], "predecessor_receipts": list(self.predecessor_receipts), "active": self.active, "historical_reproduction_preserved": self.historical_reproduction_preserved, "production_ready": False, "certified": False}

    @property
    def receipt_identity(self) -> str:
        return canonical_sha256(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        identity = canonical_sha256(payload)
        if identity != self._integrity_anchor:
            raise EvaluationError("MUTATED_GOVERNED_OBJECT", "receipt inputs changed after evaluation")
        payload["receipt_identity"] = identity
        return payload


def evaluate_structural_conversation(*, subject: StructuralEvaluationSubject, locks: tuple[WrongReadingLock, ...], dimensions: tuple[IndependentDimensionResult, ...], human_owned_artifacts: tuple[HumanOwnedArtifactApplicability, ...], predecessor_receipts: tuple[str, ...]) -> StructuralConversationalEvaluationReceipt:
    if subject.consent_state == "ASSUMED_FROM_SILENCE":
        raise EvaluationError("CONSENT_CANNOT_BE_INFERRED_FROM_SILENCE", "silence is not consent")
    if subject.consent_state is ConsentState.WITHDRAWN and subject.evidence_active:
        raise EvaluationError("WITHDRAWN_EVIDENCE_CANNOT_REMAIN_ACTIVE", "withdrawn evidence must become inactive")
    if subject.response_ownership != "HUMAN_OWNED_EXTERNAL_NOT_PROVIDED":
        raise EvaluationError("HUMAN_RESPONSE_OWNERSHIP_VIOLATION", "actual response authority remains human-owned and external")
    artifact_kinds = tuple(item.artifact_kind for item in human_owned_artifacts)
    required_artifacts = {"ReactionReceipt", "ExpressionMoment", "IdentityDNAAmendmentApproval"}
    if set(artifact_kinds) != required_artifacts or len(artifact_kinds) != len(required_artifacts):
        raise EvaluationError("INCOMPLETE_HUMAN_OWNED_ARTIFACT_APPLICABILITY", "all human-owned artifacts require an explicit state")
    dominant = tuple(item for item in locks if item.dominant)
    if not dominant:
        raise EvaluationError("MISSING_DOMINANT_WRONG_READING_LOCK", "at least one dominant lock is required")
    ids = tuple(item.dimension_id for item in dimensions)
    if len(ids) != len(set(ids)):
        raise EvaluationError("DUPLICATE_CONVERSATIONAL_DIMENSION", "each dimension must appear once")
    unknown = tuple(item for item in ids if item not in CONVERSATIONAL_DIMENSION_IDS)
    if unknown:
        raise EvaluationError("UNSUPPORTED_CONVERSATIONAL_DIMENSION", "unknown dimension", unsupported_dimensions=unknown)
    missing = tuple(item for item in CONVERSATIONAL_DIMENSION_IDS if item not in ids)
    if missing:
        raise EvaluationError("INCOMPLETE_CONVERSATIONAL_DIMENSION_COVERAGE", "all eleven dimensions are required", missing_dimensions=missing)
    matches = tuple(WrongReadingLockResult(item.lock_id, subject.proposed_reading.casefold().strip() == item.prohibited_reading.casefold().strip(), item.protected_meaning_ref.sha256) for item in locks)
    withdrawn = subject.consent_state is ConsentState.WITHDRAWN
    wrong_reading_failed = any(item.matched for item in matches) or any(item.dimension_id == "wrong_reading_rejection" and item.status is DimensionStatus.FAIL for item in dimensions)
    other_failed = any(item.dimension_id != "wrong_reading_rejection" and item.status is DimensionStatus.FAIL for item in dimensions)
    if withdrawn:
        decision = EvaluationDecision.BLOCKED_HUMAN_EVIDENCE_REQUIRED
    elif wrong_reading_failed:
        decision = EvaluationDecision.FAIL_WRONG_READING_LOCK
    elif other_failed:
        decision = EvaluationDecision.FAIL_STRUCTURAL_DIMENSION
    else:
        decision = EvaluationDecision.PASS_STRUCTURAL_DEVELOPMENT_ONLY
    return StructuralConversationalEvaluationReceipt(subject, decision, matches, tuple(dimensions), tuple(human_owned_artifacts), tuple(predecessor_receipts), decision is EvaluationDecision.PASS_STRUCTURAL_DEVELOPMENT_ONLY and subject.evidence_active)


def evaluate_structural_conversational(*args: Any, **kwargs: Any) -> StructuralConversationalEvaluationReceipt:
    if "dimension_results" in kwargs and "dimensions" not in kwargs:
        kwargs["dimensions"] = kwargs.pop("dimension_results")
    return evaluate_structural_conversation(*args, **kwargs)


class StructuralEvaluationAction(str, Enum):
    ISSUE = "ISSUE"
    INVALIDATE = "INVALIDATE"


class StructuralAuthorityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True)
class StructuralEvaluationAuthority:
    authority_id: str
    version: str
    sha256: str
    permitted_actions: tuple[StructuralEvaluationAction, ...]
    status: StructuralAuthorityStatus = StructuralAuthorityStatus.ACTIVE

    def __post_init__(self) -> None:
        _text(self.authority_id, "authority_id")
        _text(self.version, "version")
        _sha(self.sha256, "sha256")
        if not self.permitted_actions:
            raise EvaluationError("MISSING_AUTHORITY", "permitted actions required")

    @property
    def authority_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {"authority_id": self.authority_id, "version": self.version, "sha256": self.sha256, "permitted_actions": [item.value for item in self.permitted_actions], "status": self.status.value}


@dataclass(frozen=True)
class StructuralEvaluationCommand:
    command_id: str
    action: StructuralEvaluationAction
    resource_id: str
    payload_sha256: str
    expected_authority_identity: str

    @property
    def command_identity(self) -> str:
        return canonical_sha256({"command_id": self.command_id, "action": self.action.value, "resource_id": self.resource_id, "payload_sha256": self.payload_sha256, "expected_authority_identity": self.expected_authority_identity})


@dataclass(frozen=True)
class StructuralEvaluationInvalidationReceipt:
    prior_receipt_identity: str
    affected_scope: tuple[str, ...]
    active_after: bool
    historical_reproduction_preserved: bool
    command_identity: str
    authority_identity: str

    @property
    def invalidation_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {"prior_receipt_identity": self.prior_receipt_identity, "affected_scope": list(self.affected_scope), "active_after": self.active_after, "historical_reproduction_preserved": self.historical_reproduction_preserved, "command_identity": self.command_identity, "authority_identity": self.authority_identity}


def compute_structural_issue_payload_sha256(receipt: StructuralConversationalEvaluationReceipt) -> str:
    return canonical_sha256(receipt.as_dict())


def compute_structural_invalidation_payload_sha256(prior_receipt_identity: str, affected_scope: tuple[str, ...]) -> str:
    return canonical_sha256({"prior_receipt_identity": prior_receipt_identity, "affected_scope": list(affected_scope)})


def _validate_command(command: StructuralEvaluationCommand, action: StructuralEvaluationAction, resource_id: str, payload_sha256: str, authority: StructuralEvaluationAuthority) -> None:
    if authority.status is not StructuralAuthorityStatus.ACTIVE:
        raise EvaluationError("INACTIVE_AUTHORITY", "authority is not active")
    if action not in authority.permitted_actions or command.action is not action:
        raise EvaluationError("UNAUTHORIZED_ACTION", "action not permitted")
    if command.resource_id != resource_id:
        raise EvaluationError("COMMAND_RESOURCE_MISMATCH", "resource mismatch")
    if command.payload_sha256 != payload_sha256:
        raise EvaluationError("COMMAND_PAYLOAD_MISMATCH", "payload mismatch")
    if command.expected_authority_identity != authority.authority_identity:
        raise EvaluationError("AUTHORITY_IDENTITY_MISMATCH", "authority mismatch")


def issue_structural_evaluation_receipt(receipt: StructuralConversationalEvaluationReceipt, command: StructuralEvaluationCommand, authority: StructuralEvaluationAuthority) -> StructuralConversationalEvaluationReceipt:
    _validate_command(command, StructuralEvaluationAction.ISSUE, receipt.receipt_identity, compute_structural_issue_payload_sha256(receipt), authority)
    return receipt


def validate_repeat_structural_evaluation(existing: StructuralConversationalEvaluationReceipt, repeated: StructuralConversationalEvaluationReceipt) -> StructuralConversationalEvaluationReceipt:
    existing.as_dict()
    repeated.as_dict()
    if existing.receipt_identity != repeated.receipt_identity:
        raise EvaluationError("CONFLICTING_REPEAT_COMMAND", "repeat payload differs")
    return existing


def invalidate_structural_evaluation_receipt(receipt: StructuralConversationalEvaluationReceipt, command: StructuralEvaluationCommand, authority: StructuralEvaluationAuthority, affected_scope: tuple[str, ...]) -> StructuralEvaluationInvalidationReceipt:
    receipt.as_dict()
    if not affected_scope:
        raise EvaluationError("MISSING_GOVERNED_FIELD", "affected_scope required")
    payload = compute_structural_invalidation_payload_sha256(receipt.receipt_identity, affected_scope)
    _validate_command(command, StructuralEvaluationAction.INVALIDATE, receipt.receipt_identity, payload, authority)
    return StructuralEvaluationInvalidationReceipt(receipt.receipt_identity, tuple(affected_scope), False, True, command.command_identity, authority.authority_identity)
