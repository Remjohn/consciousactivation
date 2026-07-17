from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from cmf_builder.domain.category_runtime_rules import (
    CategoryOperatingRules,
    RULESET_MATURITY,
)
from cmf_builder.domain.category_syntax import (
    ACTIVATION_FIRST,
    CONVERSATIONAL_PROFILES,
    VISUAL_SYNTAX_FIRST,
    GovernedRef,
)


CONVERSATIONAL_CATEGORY_ID = "conversational_activation_expression"
FEEDBACK_MATURITY = "STRUCTURAL_NON_PERSONAL_UNCERTIFIED"
TERMINAL_STATES = frozenset({"CLOSED_NO_RESPONSE", "WITHDRAWN", "INVALIDATED"})
_IMMUTABLE_VERSION = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
PROFILE_APPLICABILITY: Mapping[str, tuple[str, str]] = {
    "public_comment": ("OPTIONAL_EXTERNAL_REFERENCE", "NOT_APPLICABLE"),
    "reply_dm": ("REQUIRED_EXTERNAL_REFERENCE", "OPTIONAL_EXTERNAL_REFERENCE"),
    "reelcast_expression": (
        "REQUIRED_EXTERNAL_REFERENCE",
        "REQUIRED_EXTERNAL_REFERENCE",
    ),
    "interview_expression": (
        "REQUIRED_EXTERNAL_REFERENCE",
        "REQUIRED_EXTERNAL_REFERENCE",
    ),
}


class ConversationalFeedbackError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ConversationalFeedbackInput:
    chain_id: str
    chain_version: str
    category_policy: CategoryOperatingRules
    activative_pack_ref: GovernedRef
    consent_policy_ref: GovernedRef
    source_human_authority_ref: GovernedRef
    capture_authority_ref: GovernedRef
    call_constraints: tuple[str, ...]
    desired_human_role: str
    desired_reaction: str
    micro_commitment: str
    wrong_reading_locks: tuple[str, ...]
    reaction_receipt_ref: GovernedRef | None = None
    expression_moment_ref: GovernedRef | None = None
    scripted_human_landing: str | None = None
    identity_dna_approval_requested: bool = False
    production_ready: bool = False
    certified: bool = False

    def canonical_dict(self) -> dict[str, object]:
        return {
            "chain_id": self.chain_id,
            "chain_version": self.chain_version,
            "category_policy_hash": self.category_policy.ruleset_hash,
            "activative_pack_ref": self.activative_pack_ref.canonical_dict(),
            "consent_policy_ref": self.consent_policy_ref.canonical_dict(),
            "source_human_authority_ref": self.source_human_authority_ref.canonical_dict(),
            "capture_authority_ref": self.capture_authority_ref.canonical_dict(),
            "call_constraints": list(self.call_constraints),
            "desired_human_role": self.desired_human_role,
            "desired_reaction": self.desired_reaction,
            "micro_commitment": self.micro_commitment,
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "reaction_receipt_ref": _optional_ref(self.reaction_receipt_ref),
            "expression_moment_ref": _optional_ref(self.expression_moment_ref),
            "scripted_human_landing": self.scripted_human_landing,
            "identity_dna_approval_requested": self.identity_dna_approval_requested,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class ActivativeCallContract:
    call_id: str
    profile_id: str
    pack_ref: GovernedRef
    constraints: tuple[str, ...]
    desired_human_role: str
    desired_reaction: str
    micro_commitment: str
    wrong_reading_locks: tuple[str, ...]
    execution_owner: str
    call_hash: str

    def canonical_dict(self) -> dict[str, object]:
        return {
            "call_id": self.call_id,
            "profile_id": self.profile_id,
            "pack_ref": self.pack_ref.canonical_dict(),
            "constraints": list(self.constraints),
            "desired_human_role": self.desired_human_role,
            "desired_reaction": self.desired_reaction,
            "micro_commitment": self.micro_commitment,
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "execution_owner": self.execution_owner,
            "call_hash": self.call_hash,
        }


@dataclass(frozen=True, slots=True)
class HumanResponseRequestContract:
    request_id: str
    call_hash: str
    source_human_authority_ref: GovernedRef
    capture_authority_ref: GovernedRef
    consent_policy_ref: GovernedRef
    request_status: str
    response_payload_permitted: bool
    request_hash: str

    def canonical_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "call_hash": self.call_hash,
            "source_human_authority_ref": self.source_human_authority_ref.canonical_dict(),
            "capture_authority_ref": self.capture_authority_ref.canonical_dict(),
            "consent_policy_ref": self.consent_policy_ref.canonical_dict(),
            "request_status": self.request_status,
            "response_payload_permitted": self.response_payload_permitted,
            "request_hash": self.request_hash,
        }


@dataclass(frozen=True, slots=True)
class ExternalFeedbackReference:
    artifact_kind: str
    applicability: str
    reference_status: str
    external_ref: GovernedRef | None
    issuance_owner: str

    def canonical_dict(self) -> dict[str, object]:
        return {
            "artifact_kind": self.artifact_kind,
            "applicability": self.applicability,
            "reference_status": self.reference_status,
            "external_ref": _optional_ref(self.external_ref),
            "issuance_owner": self.issuance_owner,
        }


@dataclass(frozen=True, slots=True)
class ConversationalFeedbackChain:
    chain_id: str
    chain_version: str
    chain_hash: str
    profile_id: str
    category_id: str
    category_policy_hash: str
    activative_call: ActivativeCallContract
    human_response_request: HumanResponseRequestContract
    reaction_receipt: ExternalFeedbackReference
    expression_moment: ExternalFeedbackReference
    state: str
    consent_status: str
    reference_use_allowed: bool
    wrong_reading_locks: tuple[str, ...]
    semantic_lineage: tuple[GovernedRef, ...]
    runtime_law: str
    development_law: str
    maturity_status: str
    human_policy_gate: str
    production_ready: bool
    certified: bool
    canonical_bytes: bytes

    def canonical_dict(self) -> dict[str, object]:
        content = json.loads(self.canonical_bytes.decode("utf-8"))
        content["chain_hash"] = self.chain_hash
        return content


@dataclass(frozen=True, slots=True)
class FeedbackTransition:
    event: str
    new_version: str
    authority_ref: GovernedRef
    reaction_receipt_ref: GovernedRef | None = None
    expression_moment_ref: GovernedRef | None = None
    reason: str = "governed structural transition"


def compile_structural_feedback_chain(
    source: ConversationalFeedbackInput,
) -> ConversationalFeedbackChain:
    _require_text(source.chain_id, "chain_id")
    _validate_immutable_version(source.chain_version, "chain_version")
    _validate_policy(source.category_policy)
    if source.production_ready or source.certified:
        raise ConversationalFeedbackError(
            "The structural branch cannot claim production or certification."
        )
    if source.scripted_human_landing is not None:
        raise ConversationalFeedbackError("A human landing cannot be scripted or inferred.")
    if source.identity_dna_approval_requested:
        raise ConversationalFeedbackError(
            "Identity DNA approval remains with human identity authority."
        )
    profile_id = source.category_policy.profile_id
    if profile_id not in CONVERSATIONAL_PROFILES:
        raise ConversationalFeedbackError("A governed conversational profile is required.")
    _validate_ref(source.activative_pack_ref, "activative_intelligence_pack")
    _validate_ref(source.consent_policy_ref, "consent_policy")
    _validate_ref(source.source_human_authority_ref, "source_human_authority")
    _validate_ref(source.capture_authority_ref, "capture_authority")
    constraints = _unique_texts(source.call_constraints, "call_constraints")
    locks = tuple(sorted(_unique_texts(source.wrong_reading_locks, "wrong_reading_locks")))
    desired_role = _require_text(source.desired_human_role, "desired_human_role")
    desired_reaction = _require_text(source.desired_reaction, "desired_reaction")
    micro_commitment = _require_text(source.micro_commitment, "micro_commitment")
    reaction_applicability, expression_applicability = PROFILE_APPLICABILITY[profile_id]
    reaction = _feedback_reference(
        "ReactionReceipt", reaction_applicability, source.reaction_receipt_ref
    )
    expression = _feedback_reference(
        "ExpressionMoment", expression_applicability, source.expression_moment_ref
    )
    call = _build_call(
        profile_id=profile_id,
        pack_ref=source.activative_pack_ref,
        constraints=constraints,
        desired_human_role=desired_role,
        desired_reaction=desired_reaction,
        micro_commitment=micro_commitment,
        locks=locks,
    )
    request = _build_request(
        call_hash=call.call_hash,
        source_human_authority_ref=source.source_human_authority_ref,
        capture_authority_ref=source.capture_authority_ref,
        consent_policy_ref=source.consent_policy_ref,
        request_status="STRUCTURAL_REQUEST_NOT_SENT",
    )
    lineage = _sorted_unique_refs(
        (
            source.activative_pack_ref,
            source.consent_policy_ref,
            source.source_human_authority_ref,
            source.capture_authority_ref,
        )
        + tuple(
            ref
            for ref in (source.reaction_receipt_ref, source.expression_moment_ref)
            if ref is not None
        )
    )
    return _build_chain(
        chain_id=source.chain_id,
        chain_version=source.chain_version,
        profile_id=profile_id,
        category_policy_hash=source.category_policy.ruleset_hash,
        call=call,
        request=request,
        reaction=reaction,
        expression=expression,
        state="STRUCTURAL_COMPILED",
        consent_status="POLICY_REFERENCE_ACTIVE_NO_PERSONAL_DATA_COLLECTED",
        reference_use_allowed=True,
        locks=locks,
        lineage=lineage,
    )


def transition_feedback_chain(
    chain: ConversationalFeedbackChain, transition: FeedbackTransition
) -> ConversationalFeedbackChain:
    _validate_immutable_version(transition.new_version, "transition.new_version")
    if chain.state in TERMINAL_STATES:
        raise ConversationalFeedbackError("A terminal feedback chain cannot transition.")
    if transition.new_version == chain.chain_version:
        raise ConversationalFeedbackError("A transition requires a new immutable version.")
    transition.authority_ref.validate()
    _require_text(transition.reason, "transition.reason")
    if transition.event == "REQUEST_HUMAN_RESPONSE":
        _validate_transition_authority(
            transition.authority_ref,
            chain.human_response_request.capture_authority_ref,
        )
        if chain.state != "STRUCTURAL_COMPILED":
            raise ConversationalFeedbackError("A response request is not valid in this state.")
        request = _replace_request_status(chain.human_response_request, "EXTERNAL_REQUEST_PENDING")
        return _rebuild(
            chain,
            new_version=transition.new_version,
            request=request,
            state="AWAITING_EXTERNAL_HUMAN_RESPONSE",
            lineage_add=(transition.authority_ref,),
        )
    if transition.event == "REGISTER_EXTERNAL_REFERENCES":
        _validate_transition_authority(
            transition.authority_ref,
            chain.human_response_request.capture_authority_ref,
        )
        if (
            transition.reaction_receipt_ref is None
            and transition.expression_moment_ref is None
        ):
            raise ConversationalFeedbackError(
                "At least one external immutable feedback reference is required."
            )
        reaction = _feedback_reference(
            "ReactionReceipt",
            chain.reaction_receipt.applicability,
            transition.reaction_receipt_ref,
        )
        expression = _feedback_reference(
            "ExpressionMoment",
            chain.expression_moment.applicability,
            transition.expression_moment_ref,
        )
        _require_applicable_external_refs(reaction, expression)
        refs = tuple(
            ref
            for ref in (
                transition.authority_ref,
                transition.reaction_receipt_ref,
                transition.expression_moment_ref,
            )
            if ref is not None
        )
        return _rebuild(
            chain,
            new_version=transition.new_version,
            reaction=reaction,
            expression=expression,
            state="EXTERNAL_REFERENCES_AVAILABLE",
            lineage_add=refs,
        )
    if transition.event == "MARK_RECOMPILE_ELIGIBLE":
        if chain.state != "EXTERNAL_REFERENCES_AVAILABLE":
            raise ConversationalFeedbackError(
                "Recompile eligibility requires external reference availability."
            )
        _validate_transition_authority(
            transition.authority_ref,
            chain.human_response_request.capture_authority_ref,
        )
        return _rebuild(
            chain,
            new_version=transition.new_version,
            state="RECOMPILE_ELIGIBLE_REFERENCE_ONLY",
            lineage_add=(transition.authority_ref,),
        )
    if transition.event == "WITHDRAW_CONSENT":
        _validate_transition_authority(
            transition.authority_ref,
            chain.human_response_request.source_human_authority_ref,
        )
        request = _replace_request_status(chain.human_response_request, "WITHDRAWN")
        return _rebuild(
            chain,
            new_version=transition.new_version,
            request=request,
            state="WITHDRAWN",
            consent_status="WITHDRAWN",
            reference_use_allowed=False,
            lineage_add=(transition.authority_ref,),
        )
    if transition.event == "INVALIDATE_UPSTREAM":
        _validate_invalidation_authority(transition.authority_ref, chain)
        return _rebuild(
            chain,
            new_version=transition.new_version,
            state="INVALIDATED",
            reference_use_allowed=False,
            lineage_add=(transition.authority_ref,),
        )
    if transition.event == "CLOSE_WITHOUT_RESPONSE":
        _validate_transition_authority(
            transition.authority_ref,
            chain.human_response_request.capture_authority_ref,
        )
        request = _replace_request_status(chain.human_response_request, "CLOSED_NO_RESPONSE")
        return _rebuild(
            chain,
            new_version=transition.new_version,
            request=request,
            state="CLOSED_NO_RESPONSE",
            reference_use_allowed=False,
            lineage_add=(transition.authority_ref,),
        )
    raise ConversationalFeedbackError("Feedback transition event is unsupported.")


def _validate_policy(policy: CategoryOperatingRules) -> None:
    if policy.ruleset_hash != f"sha256:{sha256(policy.canonical_bytes).hexdigest()}":
        raise ConversationalFeedbackError("Category policy hash is altered.")
    if policy.category_id != CONVERSATIONAL_CATEGORY_ID:
        raise ConversationalFeedbackError("Only the conversational category is applicable.")
    if policy.profile_id not in CONVERSATIONAL_PROFILES:
        raise ConversationalFeedbackError("Conversational profile identity is invalid.")
    if policy.maturity_status != RULESET_MATURITY:
        raise ConversationalFeedbackError("Category policy maturity is unsupported.")
    if policy.external_handoff_boundary.mode != "BUILDER_CONTRACT_ONLY":
        raise ConversationalFeedbackError("External runtime ownership boundary is invalid.")
    if policy.production_ready or policy.certified:
        raise ConversationalFeedbackError("Policy cannot carry readiness or certification.")


def _validate_ref(ref: GovernedRef, expected_role: str) -> None:
    ref.validate()
    if ref.lineage_role != expected_role:
        raise ConversationalFeedbackError(f"Expected {expected_role} reference authority.")


def _feedback_reference(
    artifact_kind: str,
    applicability: str,
    ref: GovernedRef | None,
) -> ExternalFeedbackReference:
    if applicability == "NOT_APPLICABLE":
        if ref is not None:
            raise ConversationalFeedbackError(
                f"{artifact_kind} cannot be supplied when NOT_APPLICABLE."
            )
        return ExternalFeedbackReference(
            artifact_kind,
            applicability,
            "NOT_APPLICABLE",
            None,
            "EXTERNAL_HUMAN_CAPTURE_AUTHORITY",
        )
    if ref is not None:
        expected = "reaction_receipt" if artifact_kind == "ReactionReceipt" else "expression_moment"
        _validate_ref(ref, expected)
        status = "EXTERNAL_IMMUTABLE_REFERENCE_PRESENT"
    else:
        status = "PENDING_EXTERNAL_HUMAN_EVIDENCE"
    return ExternalFeedbackReference(
        artifact_kind,
        applicability,
        status,
        ref,
        "EXTERNAL_HUMAN_CAPTURE_AUTHORITY",
    )


def _require_applicable_external_refs(
    reaction: ExternalFeedbackReference, expression: ExternalFeedbackReference
) -> None:
    if expression.external_ref is not None and reaction.external_ref is None:
        raise ConversationalFeedbackError(
            "ExpressionMoment reference requires its external ReactionReceipt reference."
        )
    for item in (reaction, expression):
        if item.applicability == "REQUIRED_EXTERNAL_REFERENCE" and item.external_ref is None:
            raise ConversationalFeedbackError(
                f"{item.artifact_kind} requires an external immutable reference."
            )


def _build_call(
    *,
    profile_id: str,
    pack_ref: GovernedRef,
    constraints: tuple[str, ...],
    desired_human_role: str,
    desired_reaction: str,
    micro_commitment: str,
    locks: tuple[str, ...],
) -> ActivativeCallContract:
    content = {
        "profile_id": profile_id,
        "pack_ref": pack_ref.canonical_dict(),
        "constraints": list(constraints),
        "desired_human_role": desired_human_role,
        "desired_reaction": desired_reaction,
        "micro_commitment": micro_commitment,
        "wrong_reading_locks": list(locks),
        "execution_owner": "EXTERNAL_CONVERSATIONAL_HARNESS",
    }
    digest = sha256(_canonical_json(content)).hexdigest()
    return ActivativeCallContract(
        call_id=f"activative-call-contract_{digest}",
        profile_id=profile_id,
        pack_ref=pack_ref,
        constraints=constraints,
        desired_human_role=desired_human_role,
        desired_reaction=desired_reaction,
        micro_commitment=micro_commitment,
        wrong_reading_locks=locks,
        execution_owner="EXTERNAL_CONVERSATIONAL_HARNESS",
        call_hash=f"sha256:{digest}",
    )


def _build_request(
    *,
    call_hash: str,
    source_human_authority_ref: GovernedRef,
    capture_authority_ref: GovernedRef,
    consent_policy_ref: GovernedRef,
    request_status: str,
) -> HumanResponseRequestContract:
    content = {
        "call_hash": call_hash,
        "source_human_authority_ref": source_human_authority_ref.canonical_dict(),
        "capture_authority_ref": capture_authority_ref.canonical_dict(),
        "consent_policy_ref": consent_policy_ref.canonical_dict(),
        "request_status": request_status,
        "response_payload_permitted": False,
    }
    digest = sha256(_canonical_json(content)).hexdigest()
    return HumanResponseRequestContract(
        request_id=f"human-response-request_{digest}",
        call_hash=call_hash,
        source_human_authority_ref=source_human_authority_ref,
        capture_authority_ref=capture_authority_ref,
        consent_policy_ref=consent_policy_ref,
        request_status=request_status,
        response_payload_permitted=False,
        request_hash=f"sha256:{digest}",
    )


def _replace_request_status(
    request: HumanResponseRequestContract, status: str
) -> HumanResponseRequestContract:
    return _build_request(
        call_hash=request.call_hash,
        source_human_authority_ref=request.source_human_authority_ref,
        capture_authority_ref=request.capture_authority_ref,
        consent_policy_ref=request.consent_policy_ref,
        request_status=status,
    )


def _build_chain(
    *,
    chain_id: str,
    chain_version: str,
    profile_id: str,
    category_policy_hash: str,
    call: ActivativeCallContract,
    request: HumanResponseRequestContract,
    reaction: ExternalFeedbackReference,
    expression: ExternalFeedbackReference,
    state: str,
    consent_status: str,
    reference_use_allowed: bool,
    locks: tuple[str, ...],
    lineage: tuple[GovernedRef, ...],
) -> ConversationalFeedbackChain:
    content: dict[str, object] = {
        "schema_version": "cmf-builder-conversational-feedback-chain/v1",
        "chain_id": chain_id,
        "chain_version": chain_version,
        "profile_id": profile_id,
        "category_id": CONVERSATIONAL_CATEGORY_ID,
        "category_policy_hash": category_policy_hash,
        "activative_call": call.canonical_dict(),
        "human_response_request": request.canonical_dict(),
        "reaction_receipt": reaction.canonical_dict(),
        "expression_moment": expression.canonical_dict(),
        "state": state,
        "consent_status": consent_status,
        "reference_use_allowed": reference_use_allowed,
        "wrong_reading_locks": list(locks),
        "semantic_lineage": [ref.canonical_dict() for ref in lineage],
        "runtime_law": ACTIVATION_FIRST,
        "development_law": VISUAL_SYNTAX_FIRST,
        "maturity_status": FEEDBACK_MATURITY,
        "human_policy_gate": "HD-006:HUMAN_POLICY_PENDING;HD-007:CERTIFICATION_PENDING",
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return ConversationalFeedbackChain(
        chain_id=chain_id,
        chain_version=chain_version,
        chain_hash=f"sha256:{digest}",
        profile_id=profile_id,
        category_id=CONVERSATIONAL_CATEGORY_ID,
        category_policy_hash=category_policy_hash,
        activative_call=call,
        human_response_request=request,
        reaction_receipt=reaction,
        expression_moment=expression,
        state=state,
        consent_status=consent_status,
        reference_use_allowed=reference_use_allowed,
        wrong_reading_locks=locks,
        semantic_lineage=lineage,
        runtime_law=ACTIVATION_FIRST,
        development_law=VISUAL_SYNTAX_FIRST,
        maturity_status=FEEDBACK_MATURITY,
        human_policy_gate="HD-006:HUMAN_POLICY_PENDING;HD-007:CERTIFICATION_PENDING",
        production_ready=False,
        certified=False,
        canonical_bytes=canonical_bytes,
    )


def _rebuild(
    chain: ConversationalFeedbackChain,
    *,
    new_version: str,
    request: HumanResponseRequestContract | None = None,
    reaction: ExternalFeedbackReference | None = None,
    expression: ExternalFeedbackReference | None = None,
    state: str,
    consent_status: str | None = None,
    reference_use_allowed: bool | None = None,
    lineage_add: tuple[GovernedRef, ...] = (),
) -> ConversationalFeedbackChain:
    return _build_chain(
        chain_id=chain.chain_id,
        chain_version=new_version,
        profile_id=chain.profile_id,
        category_policy_hash=chain.category_policy_hash,
        call=chain.activative_call,
        request=request or chain.human_response_request,
        reaction=reaction or chain.reaction_receipt,
        expression=expression or chain.expression_moment,
        state=state,
        consent_status=consent_status or chain.consent_status,
        reference_use_allowed=(
            chain.reference_use_allowed
            if reference_use_allowed is None
            else reference_use_allowed
        ),
        locks=chain.wrong_reading_locks,
        lineage=_sorted_unique_refs(chain.semantic_lineage + lineage_add),
    )


def _validate_transition_authority(observed: GovernedRef, expected: GovernedRef) -> None:
    if observed != expected:
        raise ConversationalFeedbackError("Transition authority is not attributable.")


def _validate_invalidation_authority(
    observed: GovernedRef, chain: ConversationalFeedbackChain
) -> None:
    observed.validate()
    exact_chain_authorities = tuple(
        ref
        for ref in chain.semantic_lineage
        if ref.lineage_role in {"capture_authority", "constitutional_authority"}
    )
    if observed not in exact_chain_authorities:
        raise ConversationalFeedbackError(
            "Upstream invalidation requires an exact governed chain authority."
        )


def _sorted_unique_refs(refs: tuple[GovernedRef, ...]) -> tuple[GovernedRef, ...]:
    keys = [(ref.lineage_role, ref.object_id, ref.version, ref.sha256) for ref in refs]
    if len(set(keys)) != len(keys):
        # Repeated authority use is lineage-preserving rather than a new evidence item.
        unique = {key: ref for key, ref in zip(keys, refs)}
        refs = tuple(unique.values())
    return tuple(
        sorted(
            refs,
            key=lambda ref: (ref.lineage_role, ref.object_id, ref.version, ref.sha256),
        )
    )


def _unique_texts(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    if not values:
        raise ConversationalFeedbackError(f"{field} must be non-empty.")
    normalized = tuple(_require_text(value, field) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ConversationalFeedbackError(f"{field} contains duplicates.")
    return normalized


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConversationalFeedbackError(f"{field} must be a non-empty string.")
    return value.strip()


def _validate_immutable_version(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ConversationalFeedbackError(
            f"{field} must be a valid immutable semantic version."
        )
    normalized = value.strip()
    if (
        not normalized
        or normalized != value
        or _IMMUTABLE_VERSION.fullmatch(normalized) is None
    ):
        raise ConversationalFeedbackError(
            f"{field} must be a valid immutable semantic version."
        )
    return normalized


def _optional_ref(ref: GovernedRef | None) -> dict[str, str] | None:
    return None if ref is None else ref.canonical_dict()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
