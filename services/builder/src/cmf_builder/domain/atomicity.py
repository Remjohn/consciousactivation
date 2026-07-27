from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


class AtomicityError(Exception):
    code = "AtomicityError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class BoundaryInputHashMismatch(AtomicityError):
    code = "BoundaryInputHashMismatch"


class BoundaryInputInvalid(AtomicityError):
    code = "BoundaryInputInvalid"


class BoundaryInputMismatch(AtomicityError):
    code = "BoundaryInputMismatch"


class DecisionPackageIncomplete(AtomicityError):
    code = "DecisionPackageIncomplete"


class CriticalBoundaryContradiction(AtomicityError):
    code = "CriticalBoundaryContradiction"


class BoundaryImmutable(AtomicityError):
    code = "BoundaryImmutable"


class FieldAuthorityRejected(AtomicityError):
    code = "FieldAuthorityRejected"


class AtomicityDecisionAction(str, Enum):
    APPROVE = "APPROVE"
    REVISE = "REVISE"
    REJECT = "REJECT"


class BoundaryStatus(str, Enum):
    DECLARED_UNRATIFIED = "DECLARED_UNRATIFIED"
    FROZEN = "FROZEN"


class ModelStatus(str, Enum):
    UNRATIFIED_CONSTITUTIONAL_FIELDS = "UNRATIFIED_CONSTITUTIONAL_FIELDS"


class AuthorityStatus(str, Enum):
    HUMAN_RATIFIED = "HUMAN_RATIFIED"
    SOURCE_LOCKED = "SOURCE_LOCKED"
    UNRATIFIED = "UNRATIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class KnowledgeStatus(str, Enum):
    LOCKED_EVIDENCE = "LOCKED_EVIDENCE"
    HYPOTHESIS = "HYPOTHESIS"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class AlternativeCandidate:
    candidate_id: str
    proposed_disposition: str
    reason: str


@dataclass(frozen=True, slots=True)
class DeclaredBoundaryInput:
    input_id: str
    version: str
    input_hash: str
    synthetic: bool
    repository_owned: bool
    category_binding: str
    production_eligible: bool
    certified: bool
    purpose: str
    source_profile_ref: str
    source_profile_hash: str
    target_profile_ref: str
    target_candidate_ref: str
    target_candidate_hash: str
    candidate_id: str
    boundary: str
    production_promise: str
    inputs: tuple[tuple[tuple[str, object], ...], ...]
    outputs: tuple[tuple[tuple[str, object], ...], ...]
    invariants: tuple[str, ...]
    legal_variation: tuple[str, ...]
    capabilities: tuple[str, ...]
    category_ownership: str
    critical_contradictions: tuple[str, ...]
    alternative_candidates: tuple[AlternativeCandidate, ...]
    locked_evidence_fields: tuple[str, ...]
    not_applicable_fields: tuple[str, ...]
    hypothesis_fields: tuple[str, ...]
    initial_model_status: str
    initial_boundary_status: str
    allowed_actions: tuple[str, ...]
    approval_requires: tuple[str, ...]
    amendment_rule: str

    @property
    def boundary_ref(self) -> str:
        return f"{self.input_id}@{self.version}"

    @property
    def alternative_ids(self) -> tuple[str, ...]:
        return tuple(item.candidate_id for item in self.alternative_candidates)

    @classmethod
    def from_json_bytes(
        cls, content: bytes, *, observed_sha256: str | None = None
    ) -> "DeclaredBoundaryInput":
        digest = sha256(content).hexdigest()
        if observed_sha256 is not None and digest != observed_sha256:
            raise BoundaryInputHashMismatch(
                "Declared boundary bytes do not match the capsule hash.",
                expected_sha256=observed_sha256,
                observed_sha256=digest,
            )
        try:
            value = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise BoundaryInputInvalid(
                "Declared boundary input is not valid UTF-8 JSON."
            ) from error
        if not isinstance(value, dict):
            raise BoundaryInputInvalid("Declared boundary input must be an object.")
        try:
            classification = _mapping(value, "classification")
            source = _mapping(value, "source_lock_constraints")
            candidate = _mapping(value, "candidate")
            field_policy = _mapping(value, "draft_field_policy")
            human = _mapping(value, "human_decision_required")
            result = cls(
                input_id=_text(value, "input_id"),
                version=_text(value, "version"),
                input_hash=digest,
                synthetic=_boolean(classification, "synthetic"),
                repository_owned=_boolean(classification, "repository_owned"),
                category_binding=_text(classification, "category_binding"),
                production_eligible=_boolean(classification, "production_eligible"),
                certified=_boolean(classification, "certified"),
                purpose=_text(classification, "purpose"),
                source_profile_ref=_text(source, "source_profile_ref"),
                source_profile_hash=_hash(source, "source_profile_sha256"),
                target_profile_ref=_text(source, "target_profile_ref"),
                target_candidate_ref=_text(source, "target_candidate_ref"),
                target_candidate_hash=_hash(source, "target_candidate_sha256"),
                candidate_id=_text(candidate, "candidate_id"),
                boundary=_text(candidate, "boundary"),
                production_promise=_text(candidate, "production_promise"),
                inputs=_object_tuple(candidate, "inputs"),
                outputs=_object_tuple(candidate, "outputs"),
                invariants=_text_tuple(candidate, "invariants"),
                legal_variation=_text_tuple(candidate, "legal_variation"),
                capabilities=_text_tuple(candidate, "capabilities"),
                category_ownership=_text(candidate, "category_ownership"),
                critical_contradictions=_text_tuple(
                    candidate, "critical_contradictions"
                ),
                alternative_candidates=tuple(
                    AlternativeCandidate(
                        candidate_id=_text(item, "candidate_id"),
                        proposed_disposition=_text(
                            item, "disposition_before_human_decision"
                        ),
                        reason=_text(item, "reason"),
                    )
                    for item in _mapping_list(value, "alternative_candidates")
                ),
                locked_evidence_fields=_text_tuple(
                    field_policy, "locked_evidence_fields"
                ),
                not_applicable_fields=_text_tuple(
                    field_policy, "explicit_not_applicable_fields"
                ),
                hypothesis_fields=_text_tuple(
                    field_policy, "explicit_hypothesis_fields"
                ),
                initial_model_status=_text(field_policy, "initial_model_status"),
                initial_boundary_status=_text(
                    field_policy, "boundary_status_before_human_decision"
                ),
                allowed_actions=_text_tuple(human, "allowed_actions"),
                approval_requires=_text_tuple(human, "approval_requires"),
                amendment_rule=_text(value, "amendment_rule"),
            )
        except (KeyError, TypeError) as error:
            raise BoundaryInputInvalid(
                "Declared boundary input is missing a required contract field.",
                missing_field=str(error),
            ) from error
        result.validate()
        return result

    def validate(self) -> None:
        if (
            not self.synthetic
            or not self.repository_owned
            or self.production_eligible
            or self.certified
            or self.category_binding != "none"
            or self.purpose != "Builder_Core_validation_only"
            or self.initial_boundary_status != BoundaryStatus.DECLARED_UNRATIFIED.value
            or self.initial_model_status
            != ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS.value
        ):
            raise BoundaryInputInvalid(
                "The input is not the bounded category-neutral synthetic definition."
            )
        if set(self.allowed_actions) != {
            item.value for item in AtomicityDecisionAction
        }:
            raise BoundaryInputInvalid("Atomicity decision actions are incomplete.")
        required_locked = {
            "identity",
            "production_promise",
            "inputs",
            "outputs",
            "invariants",
            "legal_variation",
            "capabilities",
            "category_ownership",
        }
        if set(self.locked_evidence_fields) != required_locked:
            raise BoundaryInputInvalid("Locked evidence field policy is incomplete.")
        if len(set(self.alternative_ids)) != len(self.alternative_ids):
            raise BoundaryInputInvalid("Alternative candidate identities must be unique.")


@dataclass(frozen=True, slots=True)
class AtomicityDecision:
    action: AtomicityDecisionAction
    selected_candidate: str | None
    rejected_alternatives: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    rationale: str
    accepted_risks: tuple[str, ...]
    human_id: str
    decided_at: datetime
    revision_request: str | None = None

    @property
    def decision_hash(self) -> str:
        return f"sha256:{sha256(_canonical_json(self.canonical_dict())).hexdigest()}"

    def canonical_dict(self) -> dict[str, object]:
        return {
            "action": self.action.value,
            "selected_candidate": self.selected_candidate,
            "rejected_alternatives": self.rejected_alternatives,
            "evidence_refs": self.evidence_refs,
            "rationale": self.rationale,
            "accepted_risks": self.accepted_risks,
            "human_id": self.human_id,
            "decided_at": self.decided_at.isoformat(),
            "revision_request": self.revision_request,
        }

    def validate(self, declared: DeclaredBoundaryInput, *, actor_id: str) -> None:
        if not self.human_id.strip() or self.human_id != actor_id:
            raise DecisionPackageIncomplete(
                "Decision identity must match the authorized human actor.",
                actor_id=actor_id,
                human_id=self.human_id,
            )
        if not self.rationale.strip() or not self.evidence_refs:
            raise DecisionPackageIncomplete(
                "Decision rationale and evidence references are required."
            )
        if self.action is AtomicityDecisionAction.APPROVE:
            if (
                self.selected_candidate != declared.candidate_id
                or set(self.rejected_alternatives) != set(declared.alternative_ids)
                or not self.accepted_risks
            ):
                raise DecisionPackageIncomplete(
                    "Approval requires the exact candidate, rejected alternatives, and accepted risks."
                )
        elif self.action is AtomicityDecisionAction.REVISE:
            if not self.revision_request or not self.revision_request.strip():
                raise DecisionPackageIncomplete(
                    "A revision decision requires an explicit revision request."
                )
        elif self.action is AtomicityDecisionAction.REJECT:
            if self.selected_candidate is not None:
                raise DecisionPackageIncomplete(
                    "A rejected boundary cannot declare a selected candidate."
                )


@dataclass(frozen=True, slots=True)
class DeclaredAtomicBoundary:
    boundary_id: str
    version: str
    candidate_id: str
    boundary: str
    production_promise: str
    input_hash: str
    source_lock_ref: str
    category_binding: str
    synthetic: bool
    repository_owned: bool
    production_eligible: bool
    certified: bool
    status: BoundaryStatus
    content_hash: str

    @classmethod
    def freeze(
        cls, declared: DeclaredBoundaryInput, *, source_lock_ref: str
    ) -> "DeclaredAtomicBoundary":
        payload = {
            "boundary_id": declared.boundary_ref,
            "version": declared.version,
            "candidate_id": declared.candidate_id,
            "boundary": declared.boundary,
            "production_promise": declared.production_promise,
            "input_hash": declared.input_hash,
            "source_lock_ref": source_lock_ref,
            "category_binding": declared.category_binding,
            "synthetic": declared.synthetic,
            "repository_owned": declared.repository_owned,
            "production_eligible": declared.production_eligible,
            "certified": declared.certified,
            "status": BoundaryStatus.FROZEN.value,
        }
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(
            boundary_id=declared.boundary_ref,
            version=declared.version,
            candidate_id=declared.candidate_id,
            boundary=declared.boundary,
            production_promise=declared.production_promise,
            input_hash=declared.input_hash,
            source_lock_ref=source_lock_ref,
            category_binding=declared.category_binding,
            synthetic=declared.synthetic,
            repository_owned=declared.repository_owned,
            production_eligible=declared.production_eligible,
            certified=declared.certified,
            status=BoundaryStatus.FROZEN,
            content_hash=f"sha256:{digest}",
        )

    def require_new_version(
        self, *, candidate_version: str, candidate_boundary: str
    ) -> None:
        if candidate_boundary != self.boundary and candidate_version == self.version:
            raise BoundaryImmutable(
                "A frozen boundary cannot be rewritten at the same version.",
                boundary_id=self.boundary_id,
                current_version=self.version,
                candidate_version=candidate_version,
            )


@dataclass(frozen=True, slots=True)
class AtomicityRatification:
    ratification_id: str
    boundary_ref: str
    selected_candidate: str
    rejected_alternatives: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    source_lock_ref: str
    human_id: str
    rationale: str
    accepted_risks: tuple[str, ...]
    signed_at: datetime
    ratification_hash: str

    @classmethod
    def create(
        cls,
        *,
        ratification_id: str,
        boundary: DeclaredAtomicBoundary,
        decision: AtomicityDecision,
    ) -> "AtomicityRatification":
        payload = {
            "ratification_id": ratification_id,
            "boundary_ref": boundary.boundary_id,
            "selected_candidate": str(decision.selected_candidate),
            "rejected_alternatives": decision.rejected_alternatives,
            "evidence_refs": decision.evidence_refs,
            "source_lock_ref": boundary.source_lock_ref,
            "human_id": decision.human_id,
            "rationale": decision.rationale,
            "accepted_risks": decision.accepted_risks,
            "signed_at": decision.decided_at,
        }
        digest_payload = {**payload, "signed_at": decision.decided_at.isoformat()}
        return cls(
            **payload,
            ratification_hash=f"sha256:{sha256(_canonical_json(digest_payload)).hexdigest()}",
        )


@dataclass(frozen=True, slots=True)
class DraftHarnessField:
    name: str
    value: object
    authority_status: AuthorityStatus
    knowledge_status: KnowledgeStatus
    provenance: tuple[str, ...]
    disposition: str


@dataclass(frozen=True, slots=True)
class DraftHarnessModel:
    model_id: str
    boundary_ref: str
    source_lock_ref: str
    fields: tuple[DraftHarnessField, ...]
    unresolved_gaps: tuple[str, ...]
    alternatives: tuple[str, ...]
    decisions_required: tuple[str, ...]
    status: ModelStatus
    model_hash: str

    @classmethod
    def compile(
        cls,
        *,
        model_id: str,
        declared: DeclaredBoundaryInput,
        boundary: DeclaredAtomicBoundary,
        ratification: AtomicityRatification,
    ) -> "DraftHarnessModel":
        locked_values: dict[str, object] = {
            "identity": (
                ("input_id", declared.input_id),
                ("version", declared.version),
                ("candidate_id", declared.candidate_id),
            ),
            "production_promise": declared.production_promise,
            "inputs": declared.inputs,
            "outputs": declared.outputs,
            "invariants": declared.invariants,
            "legal_variation": declared.legal_variation,
            "capabilities": declared.capabilities,
            "category_ownership": declared.category_ownership,
        }
        fields = [
            DraftHarnessField(
                name="atomic_boundary",
                value=declared.boundary,
                authority_status=AuthorityStatus.HUMAN_RATIFIED,
                knowledge_status=KnowledgeStatus.LOCKED_EVIDENCE,
                provenance=(
                    boundary.source_lock_ref,
                    declared.input_hash,
                    ratification.ratification_hash,
                ),
                disposition="FROZEN",
            )
        ]
        fields.extend(
            DraftHarnessField(
                name=name,
                value=locked_values[name],
                authority_status=AuthorityStatus.SOURCE_LOCKED,
                knowledge_status=KnowledgeStatus.LOCKED_EVIDENCE,
                provenance=(boundary.source_lock_ref, declared.input_hash),
                disposition="LOCKED_EVIDENCE",
            )
            for name in declared.locked_evidence_fields
        )
        fields.extend(
            DraftHarnessField(
                name=name,
                value=None,
                authority_status=AuthorityStatus.NOT_APPLICABLE,
                knowledge_status=KnowledgeStatus.NOT_APPLICABLE,
                provenance=(declared.input_hash,),
                disposition="NOT_APPLICABLE_FOR_CATEGORY_NEUTRAL_SYNTHETIC_PROOF",
            )
            for name in declared.not_applicable_fields
        )
        fields.extend(
            DraftHarnessField(
                name=name,
                value=(),
                authority_status=AuthorityStatus.UNRATIFIED,
                knowledge_status=KnowledgeStatus.HYPOTHESIS,
                provenance=(declared.input_hash,),
                disposition="DECISION_REQUIRED",
            )
            for name in declared.hypothesis_fields
        )
        ordered = tuple(sorted(fields, key=lambda item: item.name))
        payload = {
            "model_id": model_id,
            "boundary_ref": boundary.boundary_id,
            "source_lock_ref": boundary.source_lock_ref,
            "fields": [
                {
                    "name": field.name,
                    "value": _json_value(field.value),
                    "authority_status": field.authority_status.value,
                    "knowledge_status": field.knowledge_status.value,
                    "provenance": field.provenance,
                    "disposition": field.disposition,
                }
                for field in ordered
            ],
            "unresolved_gaps": declared.hypothesis_fields,
            "alternatives": declared.alternative_ids,
            "decisions_required": declared.hypothesis_fields,
            "status": ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS.value,
        }
        return cls(
            model_id=model_id,
            boundary_ref=boundary.boundary_id,
            source_lock_ref=boundary.source_lock_ref,
            fields=ordered,
            unresolved_gaps=declared.hypothesis_fields,
            alternatives=declared.alternative_ids,
            decisions_required=declared.hypothesis_fields,
            status=ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS,
            model_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}",
        )

    def field(self, name: str) -> DraftHarnessField:
        for field in self.fields:
            if field.name == name:
                return field
        raise FieldAuthorityRejected("Draft Harness field does not exist.", field=name)

    def consume(self, name: str, *, required_authority: AuthorityStatus) -> object:
        field = self.field(name)
        if field.authority_status is not required_authority:
            raise FieldAuthorityRejected(
                "Draft Harness field lacks the required authority.",
                field=name,
                required_authority=required_authority.value,
                observed_authority=field.authority_status.value,
                knowledge_status=field.knowledge_status.value,
            )
        return field.value


@dataclass(frozen=True, slots=True)
class AtomicityReadinessEvaluation:
    gate_id: str
    result: str
    reason: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BoundaryInvalidation:
    invalidation_id: str
    boundary_ref: str
    model_ref: str
    reason: str
    human_id: str
    reopened_at: datetime
    new_version_required: bool
    invalidation_hash: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        boundary_ref: str,
        model_ref: str,
        reason: str,
        human_id: str,
        reopened_at: datetime,
    ) -> "BoundaryInvalidation":
        if not reason.strip():
            raise DecisionPackageIncomplete("Reopen requires an explicit rationale.")
        payload = {
            "invalidation_id": invalidation_id,
            "boundary_ref": boundary_ref,
            "model_ref": model_ref,
            "reason": reason,
            "human_id": human_id,
            "reopened_at": reopened_at.isoformat(),
            "new_version_required": True,
        }
        return cls(
            invalidation_id=invalidation_id,
            boundary_ref=boundary_ref,
            model_ref=model_ref,
            reason=reason,
            human_id=human_id,
            reopened_at=reopened_at,
            new_version_required=True,
            invalidation_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}",
        )


@dataclass(frozen=True, slots=True)
class AtomicityDecisionReceipt:
    receipt_id: str
    command_id: str
    run_id: str
    decision_status: str
    authority_identity: str
    declared_input_hash: str
    source_lock_ref: str
    boundary_ref: str | None
    model_ref: str | None
    ratification_ref: str | None
    invalidation_ref: str | None
    event_ids: tuple[str, ...]
    hg_003_result: str
    outcome: str
    receipt_hash: str

    @classmethod
    def create(
        cls,
        *,
        receipt_id: str,
        command_id: str,
        run_id: str,
        decision_status: str,
        authority_identity: str,
        declared_input_hash: str,
        source_lock_ref: str,
        boundary_ref: str | None,
        model_ref: str | None,
        ratification_ref: str | None,
        invalidation_ref: str | None,
        event_ids: tuple[str, ...],
        hg_003_result: str,
        outcome: str = "PASS",
    ) -> "AtomicityDecisionReceipt":
        payload = {
            "receipt_id": receipt_id,
            "command_id": command_id,
            "run_id": run_id,
            "decision_status": decision_status,
            "authority_identity": authority_identity,
            "declared_input_hash": declared_input_hash,
            "source_lock_ref": source_lock_ref,
            "boundary_ref": boundary_ref,
            "model_ref": model_ref,
            "ratification_ref": ratification_ref,
            "invalidation_ref": invalidation_ref,
            "event_ids": event_ids,
            "hg_003_result": hg_003_result,
            "outcome": outcome,
        }
        return cls(
            **payload,
            receipt_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}",
        )


def _mapping(value: Mapping[str, object], field: str) -> Mapping[str, object]:
    item = value[field]
    if not isinstance(item, dict):
        raise BoundaryInputInvalid("A required object is absent.", field=field)
    return item


def _mapping_list(
    value: Mapping[str, object], field: str
) -> tuple[Mapping[str, object], ...]:
    item = value[field]
    if not isinstance(item, list) or any(not isinstance(member, dict) for member in item):
        raise BoundaryInputInvalid("A required object list is absent.", field=field)
    return tuple(item)


def _text(value: Mapping[str, object], field: str) -> str:
    item = value[field]
    if not isinstance(item, str) or not item.strip():
        raise BoundaryInputInvalid("Required text is absent.", field=field)
    return item


def _hash(value: Mapping[str, object], field: str) -> str:
    item = _text(value, field)
    if len(item) != 64 or any(character not in "0123456789abcdef" for character in item):
        raise BoundaryInputInvalid("A raw lowercase SHA-256 is required.", field=field)
    return item


def _boolean(value: Mapping[str, object], field: str) -> bool:
    item = value[field]
    if not isinstance(item, bool):
        raise BoundaryInputInvalid("Required boolean is absent.", field=field)
    return item


def _text_tuple(value: Mapping[str, object], field: str) -> tuple[str, ...]:
    item = value[field]
    if not isinstance(item, list) or any(
        not isinstance(member, str) or not member.strip() for member in item
    ):
        raise BoundaryInputInvalid("A string list is required.", field=field)
    return tuple(item)


def _object_tuple(
    value: Mapping[str, object], field: str
) -> tuple[tuple[tuple[str, object], ...], ...]:
    return tuple(
        tuple(sorted((str(key), _freeze(item)) for key, item in member.items()))
        for member in _mapping_list(value, field)
    )


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _json_value(value: object) -> object:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        _json_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
