from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.implementation_plan import VerticalImplementationPlan


FEEDBACK_INPUT_PATH = (
    "development-capsules/ST-11.03/SYNTHETIC_IMPLEMENTATION_FEEDBACK_INPUT.json"
)
FEEDBACK_INPUT_SHA256 = "e70f3ef9186aa30df2ed0296ef91fe0fb3989bbbb5fe8860437f854948d5481c"
FEEDBACK_MODE = "SYNTHETIC_BUILDER_PROOF_PROPOSAL_ONLY"
FEEDBACK_PROFILE_ID = "synthetic_text_normalization_v1"
FEEDBACK_OUTCOME = "IMPLEMENTATION_FEEDBACK_GOVERNED_AS_UNRATIFIED_PROPOSAL"
PROPOSAL_STATUS = "PROPOSED_NOT_RATIFIED"
OWNED_OBLIGATIONS = ("FR-158", "FR-159")
DIRECT_DEPENDENCIES = ("ST-11.02",)
REQUIRED_FEEDBACK_KINDS = (
    "IMPLEMENTATION_DISCOVERY",
    "EVALUATION_RESULT",
    "CERTIFICATION_FEEDBACK",
)


class ImplementationFeedbackError(Exception):
    code = "ImplementationFeedbackError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ImplementationFeedbackInputInvalid(ImplementationFeedbackError):
    code = "ImplementationFeedbackInputInvalid"


class ImplementationFeedbackTraceInvalid(ImplementationFeedbackError):
    code = "ImplementationFeedbackTraceInvalid"


class ImplementationFeedbackAuthorityInvalid(ImplementationFeedbackError):
    code = "ImplementationFeedbackAuthorityInvalid"


class ImplementationFeedbackScopeInvalid(ImplementationFeedbackError):
    code = "ImplementationFeedbackScopeInvalid"


class ImplementationFeedbackInvalidatedError(ImplementationFeedbackError):
    code = "ImplementationFeedbackInvalidated"


@dataclass(frozen=True, slots=True)
class ImplementationFeedbackItem:
    feedback_id: str
    feedback_kind: str
    subject_ref: str
    subject_hash: str
    source_identity: str
    source_kind: str
    evidence_refs: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    provenance: str
    finding: str
    recommendation: str
    required_human_disposition: str
    requested_authority_mutation: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "ImplementationFeedbackItem":
        item = cls(
            feedback_id=_text(value, "feedback_id"),
            feedback_kind=_text(value, "feedback_kind"),
            subject_ref=_text(value, "subject_ref"),
            subject_hash=_text(value, "subject_hash"),
            source_identity=_text(value, "source_identity"),
            source_kind=_text(value, "source_kind"),
            evidence_refs=_texts(value, "evidence_refs"),
            evidence_hashes=_texts(value, "evidence_hashes"),
            provenance=_text(value, "provenance"),
            finding=_text(value, "finding"),
            recommendation=_text(value, "recommendation"),
            required_human_disposition=_text(value, "required_human_disposition"),
            requested_authority_mutation=(
                value.get("requested_authority_mutation") is True
            ),
        )
        item.validate()
        return item

    def validate(self) -> None:
        if (
            self.feedback_kind not in REQUIRED_FEEDBACK_KINDS
            or not _is_sha256(self.subject_hash)
            or len(self.evidence_refs) != len(self.evidence_hashes)
            or any(_is_absolute_path(item) for item in self.evidence_refs)
            or any(not _is_sha256(item) for item in self.evidence_hashes)
            or self.requested_authority_mutation
        ):
            raise ImplementationFeedbackInputInvalid(
                "Feedback must be typed, traceable, portable and proposal-only.",
                feedback_id=self.feedback_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "feedback_id": self.feedback_id,
            "feedback_kind": self.feedback_kind,
            "subject_ref": self.subject_ref,
            "subject_hash": self.subject_hash,
            "source_identity": self.source_identity,
            "source_kind": self.source_kind,
            "evidence_refs": list(self.evidence_refs),
            "evidence_hashes": list(self.evidence_hashes),
            "provenance": self.provenance,
            "finding": self.finding,
            "recommendation": self.recommendation,
            "required_human_disposition": self.required_human_disposition,
            "requested_authority_mutation": self.requested_authority_mutation,
        }


@dataclass(frozen=True, slots=True)
class AuthorityAmendmentProposal:
    proposal_id: str
    proposal_hash: str
    schema_id: str
    schema_version: str
    proposal_version: str
    active_mode: str
    profile_id: str
    run_id: str
    plan_id: str
    plan_hash: str
    capsule_id: str
    capsule_hash: str
    feedback_input_path: str
    feedback_input_hash: str
    obligation_ids: tuple[str, ...]
    dependency_order: tuple[str, ...]
    feedback_items: tuple[ImplementationFeedbackItem, ...]
    authority_identity: str
    lineage: tuple[str, ...]
    proposal_status: str
    authority_mutated: bool
    implementation_authorized: bool
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        plan: VerticalImplementationPlan,
        feedback_input: Mapping[str, object],
        authority_identity: str,
    ) -> "AuthorityAmendmentProposal":
        _validate_input_contract(feedback_input)
        items = tuple(
            ImplementationFeedbackItem.from_mapping(item)
            for item in _mappings(feedback_input, "feedback_items")
        )
        candidate = cls(
            proposal_id="pending",
            proposal_hash="pending",
            schema_id="cmf-builder-authority-amendment-proposal/v1",
            schema_version="1.0.0",
            proposal_version=_text(feedback_input, "proposal_version"),
            active_mode=FEEDBACK_MODE,
            profile_id=FEEDBACK_PROFILE_ID,
            run_id=plan.run_id,
            plan_id=plan.plan_id,
            plan_hash=plan.plan_hash,
            capsule_id=plan.capsule_id,
            capsule_hash=plan.capsule_hash,
            feedback_input_path=FEEDBACK_INPUT_PATH,
            feedback_input_hash=f"sha256:{FEEDBACK_INPUT_SHA256}",
            obligation_ids=OWNED_OBLIGATIONS,
            dependency_order=DIRECT_DEPENDENCIES,
            feedback_items=items,
            authority_identity=authority_identity,
            lineage=(
                plan.plan_hash,
                plan.capsule_hash,
                f"sha256:{FEEDBACK_INPUT_SHA256}",
            ),
            proposal_status=PROPOSAL_STATUS,
            authority_mutated=False,
            implementation_authorized=False,
            production_eligible=False,
            certified=False,
            outcome=FEEDBACK_OUTCOME,
        )
        candidate.validate(plan)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            proposal_id=f"authority-amendment-proposal_{digest}",
            proposal_hash=f"sha256:{digest}",
        )
        result.validate(plan)
        return result

    def validate(self, plan: VerticalImplementationPlan) -> None:
        if (
            self.schema_id != "cmf-builder-authority-amendment-proposal/v1"
            or self.schema_version != "1.0.0"
            or self.active_mode != FEEDBACK_MODE
            or self.profile_id != FEEDBACK_PROFILE_ID
            or self.run_id != plan.run_id
            or self.plan_id != plan.plan_id
            or self.plan_hash != plan.plan_hash
            or self.capsule_id != plan.capsule_id
            or self.capsule_hash != plan.capsule_hash
            or self.feedback_input_path != FEEDBACK_INPUT_PATH
            or self.feedback_input_hash != f"sha256:{FEEDBACK_INPUT_SHA256}"
            or self.obligation_ids != OWNED_OBLIGATIONS
            or self.dependency_order != DIRECT_DEPENDENCIES
            or tuple(item.feedback_kind for item in self.feedback_items)
            != REQUIRED_FEEDBACK_KINDS
            or len({item.feedback_id for item in self.feedback_items}) != 3
            or self.proposal_status != PROPOSAL_STATUS
            or self.authority_mutated
            or self.implementation_authorized
            or self.production_eligible
            or self.certified
            or self.outcome != FEEDBACK_OUTCOME
            or plan.implementation_authorized
            or plan.production_eligible
            or plan.certified
        ):
            raise ImplementationFeedbackTraceInvalid(
                "The amendment proposal does not preserve the exact plan and authority boundary."
            )
        for item in self.feedback_items:
            item.validate()
        if self.lineage != (
            plan.plan_hash,
            plan.capsule_hash,
            f"sha256:{FEEDBACK_INPUT_SHA256}",
        ):
            raise ImplementationFeedbackTraceInvalid("Proposal lineage is altered.")
        if self.proposal_id != "pending" or self.proposal_hash != "pending":
            digest = sha256(
                replace(
                    self, proposal_id="pending", proposal_hash="pending"
                ).canonical_bytes()
            ).hexdigest()
            if (
                self.proposal_id != f"authority-amendment-proposal_{digest}"
                or self.proposal_hash != f"sha256:{digest}"
            ):
                raise ImplementationFeedbackTraceInvalid(
                    "Proposal identity is not deterministic."
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "proposal_version": self.proposal_version,
            "active_mode": self.active_mode,
            "profile_id": self.profile_id,
            "run_id": self.run_id,
            "plan_id": self.plan_id,
            "plan_hash": self.plan_hash,
            "capsule_id": self.capsule_id,
            "capsule_hash": self.capsule_hash,
            "feedback_input_path": self.feedback_input_path,
            "feedback_input_hash": self.feedback_input_hash,
            "obligation_ids": list(self.obligation_ids),
            "dependency_order": list(self.dependency_order),
            "feedback_items": [item.canonical_dict() for item in self.feedback_items],
            "authority_identity": self.authority_identity,
            "lineage": list(self.lineage),
            "proposal_status": self.proposal_status,
            "authority_mutated": self.authority_mutated,
            "implementation_authorized": self.implementation_authorized,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class AmendmentProposalReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    proposal_id: str
    proposal_hash: str
    plan_id: str
    plan_hash: str
    authority_identity: str
    stream_version: int
    feedback_item_count: int
    obligation_count: int
    proposal_status: str
    authority_mutated: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        proposal: AuthorityAmendmentProposal,
        stream_version: int,
    ) -> "AmendmentProposalReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id="cmf-builder-authority-amendment-proposal-receipt/v1",
            command_id=command_id,
            run_id=proposal.run_id,
            proposal_id=proposal.proposal_id,
            proposal_hash=proposal.proposal_hash,
            plan_id=proposal.plan_id,
            plan_hash=proposal.plan_hash,
            authority_identity=proposal.authority_identity,
            stream_version=stream_version,
            feedback_item_count=len(proposal.feedback_items),
            obligation_count=len(proposal.obligation_ids),
            proposal_status=proposal.proposal_status,
            authority_mutated=False,
            outcome=FEEDBACK_OUTCOME,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"amendment-proposal-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(proposal)
        return result

    def validate(self, proposal: AuthorityAmendmentProposal) -> None:
        if (
            self.schema_id != "cmf-builder-authority-amendment-proposal-receipt/v1"
            or self.run_id != proposal.run_id
            or self.proposal_id != proposal.proposal_id
            or self.proposal_hash != proposal.proposal_hash
            or self.plan_id != proposal.plan_id
            or self.plan_hash != proposal.plan_hash
            or self.authority_identity != proposal.authority_identity
            or self.stream_version < 1
            or self.feedback_item_count != len(proposal.feedback_items)
            or self.obligation_count != len(proposal.obligation_ids)
            or self.proposal_status != PROPOSAL_STATUS
            or self.authority_mutated
            or self.outcome != FEEDBACK_OUTCOME
        ):
            raise ImplementationFeedbackTraceInvalid("Proposal receipt is invalid.")
        if self.receipt_id != "pending" or self.receipt_hash != "pending":
            digest = sha256(
                replace(self, receipt_id="pending", receipt_hash="pending").canonical_bytes()
            ).hexdigest()
            if (
                self.receipt_id != f"amendment-proposal-receipt_{digest}"
                or self.receipt_hash != f"sha256:{digest}"
            ):
                raise ImplementationFeedbackTraceInvalid(
                    "Proposal receipt identity is not deterministic."
                )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "proposal_id": self.proposal_id,
                "proposal_hash": self.proposal_hash,
                "plan_id": self.plan_id,
                "plan_hash": self.plan_hash,
                "authority_identity": self.authority_identity,
                "stream_version": self.stream_version,
                "feedback_item_count": self.feedback_item_count,
                "obligation_count": self.obligation_count,
                "proposal_status": self.proposal_status,
                "authority_mutated": self.authority_mutated,
                "outcome": self.outcome,
            }
        )


def _validate_input_contract(value: Mapping[str, object]) -> None:
    if (
        value.get("schema_version")
        != "cmf-builder-synthetic-implementation-feedback-input/v1"
        or value.get("story_id") != "ST-11.03"
        or value.get("active_mode") != FEEDBACK_MODE
        or value.get("profile_id") != FEEDBACK_PROFILE_ID
        or tuple(value.get("owned_obligations", ())) != OWNED_OBLIGATIONS
        or tuple(value.get("direct_dependencies", ())) != DIRECT_DEPENDENCIES
        or value.get("proposal_status") != PROPOSAL_STATUS
        or value.get("authority_mutated") is not False
        or value.get("implementation_authorized") is not False
        or value.get("production_eligible") is not False
        or value.get("certified") is not False
        or value.get("expected_outcome") != FEEDBACK_OUTCOME
    ):
        raise ImplementationFeedbackInputInvalid("Feedback input contract is invalid.")


def _mappings(value: Mapping[str, object], key: str) -> tuple[Mapping[str, object], ...]:
    raw = value.get(key)
    if not isinstance(raw, list) or not raw or any(not isinstance(item, Mapping) for item in raw):
        raise ImplementationFeedbackInputInvalid(f"{key} must contain governed mappings.")
    return tuple(raw)  # type: ignore[return-value]


def _text(value: Mapping[str, object], key: str) -> str:
    raw = value.get(key)
    if not isinstance(raw, str) or not raw.strip():
        raise ImplementationFeedbackInputInvalid(f"{key} must be non-empty text.")
    return raw


def _texts(value: Mapping[str, object], key: str) -> tuple[str, ...]:
    raw = value.get(key)
    if not isinstance(raw, list) or not raw or any(not isinstance(item, str) or not item.strip() for item in raw):
        raise ImplementationFeedbackInputInvalid(f"{key} must contain governed text.")
    return tuple(raw)


def _is_sha256(value: str) -> bool:
    if not value.startswith("sha256:") or len(value) != 71:
        return False
    try:
        int(value[7:], 16)
    except ValueError:
        return False
    return True


def _is_absolute_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return normalized.startswith("/") or ":/" in normalized


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
