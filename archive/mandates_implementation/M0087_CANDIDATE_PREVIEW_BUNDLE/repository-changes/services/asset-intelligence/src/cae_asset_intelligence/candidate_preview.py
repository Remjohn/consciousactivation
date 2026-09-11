"""M0087 — governed candidate preview and selection session.

This module is a projection over already-authorized retrieval candidates. It does not
retrieve media, infer semantic meaning, or own storyboard/VAE authority. It persists
session revisions, immutable decision receipts, and enough candidate snapshots to
reproduce why a candidate was accepted or rejected.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ca_contracts import canonical_sha256, utc_now_rfc3339

MANDATE_ID = "M0087"
POLICY_ID = "visual-candidate-auto-accept-v1"


class CandidatePreviewError(ValueError):
    """Base M0087 validation error."""


class CandidateStaleVersionError(CandidatePreviewError):
    """Candidate session version no longer matches the caller's snapshot."""


class CandidateSelectionError(CandidatePreviewError):
    """A candidate decision violates session state or candidate eligibility."""


class AutoAcceptanceBlockedError(CandidateSelectionError):
    """Automatic acceptance failed one or more deterministic gates."""


class CandidateDecision(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    AUTO_ACCEPT = "AUTO_ACCEPT"


class NavigationDirection(str, Enum):
    NEXT = "NEXT"
    PREVIOUS = "PREVIOUS"


class CandidateSourceRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    object_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)


class CandidatePreviewCard(BaseModel):
    """A render-ready candidate snapshot supplied by the authoritative retriever."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    preview_uri: str | None = None
    transcript_context: str = ""
    source_ref: CandidateSourceRef
    source_range_ms: tuple[int, int]
    duration_ms: int = Field(gt=0)
    rights_state: str = Field(min_length=1)
    confidence_bps: int = Field(ge=0, le=10000)
    semantic_fit_bps: int = Field(ge=0, le=10000)
    quality_bps: int = Field(ge=0, le=10000)
    ranking: int = Field(ge=1)
    eligible: bool
    eligibility_reasons: tuple[str, ...] = ()
    provenance: Mapping[str, str] = Field(default_factory=dict)
    source_quality_state: str = "UNKNOWN"

    @field_validator("source_range_ms")
    @classmethod
    def valid_range(cls, value: tuple[int, int]) -> tuple[int, int]:
        start, end = value
        if start < 0 or end <= start:
            raise ValueError("source_range_ms must be a positive, ordered interval")
        return value

    @model_validator(mode="after")
    def validate_provenance(self) -> "CandidatePreviewCard":
        required = {"source_version", "source_sha256"}
        missing = sorted(required - set(self.provenance))
        if missing:
            raise ValueError(f"candidate provenance missing required fields: {missing}")
        if self.provenance.get("source_version") != self.source_ref.version:
            raise ValueError("candidate provenance source_version does not match source_ref")
        if self.provenance.get("source_sha256") != self.source_ref.sha256:
            raise ValueError("candidate provenance source_sha256 does not match source_ref")
        return self

    @property
    def auto_accept_gates(self) -> dict[str, str]:
        return {
            "eligibility": "PASS" if self.eligible else "FAIL",
            "confidence": "PASS" if self.confidence_bps >= 9000 else "FAIL",
            "semantic_fit": "PASS" if self.semantic_fit_bps >= 9000 else "FAIL",
            "rights": "PASS" if self.rights_state == "CLEARED" else "FAIL",
            "provenance": "PASS" if self._provenance_complete else "FAIL",
            "quality": "PASS" if self.quality_bps >= 8000 else "FAIL",
        }

    @property
    def _provenance_complete(self) -> bool:
        return bool(
            self.provenance.get("candidate_id") in {None, self.candidate_id}
            and self.provenance.get("source_version") == self.source_ref.version
            and self.provenance.get("source_sha256") == self.source_ref.sha256
            and self.provenance.get("scene_id")
        )


class CandidatePortfolio(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    portfolio_id: str
    request_ref: dict[str, str]
    candidates: tuple[CandidatePreviewCard, ...]
    portfolio_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


class CandidateDecisionReceipt(BaseModel):
    """Immutable receipt for one selection/rejection decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str
    mandate_id: str = MANDATE_ID
    session_id: str
    request_ref: dict[str, str]
    candidate_set_ref: dict[str, str]
    selected_candidate: dict[str, Any]
    rejected_candidates: tuple[dict[str, Any], ...] = ()
    operator_ref: dict[str, Any] | None = None
    auto_selection_policy: str | None = None
    source_ref: dict[str, str]
    source_hash: str
    source_range: tuple[int, int]
    rights_state: str
    storyboard_element_ref: dict[str, str]
    revision_ref: dict[str, str]
    decision: CandidateDecision
    rationale: str | None = None
    receipt_sha256: str
    created_at: str = Field(default_factory=utc_now_rfc3339)


class CandidatePreviewSession(BaseModel):
    """Current mutable projection of an append-only candidate session."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    campaign_id: str
    workspace_id: str
    target_ref: dict[str, str]
    target_node_id: str
    request_ref: dict[str, str]
    active_portfolio_ref: dict[str, str]
    current_index: int = 0
    selected_candidate_id: str | None = None
    rejected_candidate_ids: tuple[str, ...] = ()
    seen_candidate_ids: tuple[str, ...] = ()
    status: str = "INSPECTING"
    version: int = Field(default=1, ge=1)
    promotion_ref: dict[str, str] | None = None
    last_receipt_ref: dict[str, str] | None = None
    auto_accept_policy: str = POLICY_ID


class AcceptancePolicyRegistry:
    """Registered deterministic acceptance policy used only for automatic decisions."""

    @staticmethod
    def evaluate(candidate: CandidatePreviewCard, *, policy_id: str = POLICY_ID) -> dict[str, str]:
        if policy_id != POLICY_ID:
            raise CandidateSelectionError(f"unknown automatic acceptance policy: {policy_id}")
        gates = candidate.auto_accept_gates
        failed = [key for key, result in gates.items() if result != "PASS"]
        return {**gates, "decision": "PASS" if not failed else "BLOCKED", "failed_gates": ",".join(failed)}

    @classmethod
    def assert_accept(cls, candidate: CandidatePreviewCard, *, policy_id: str = POLICY_ID) -> dict[str, str]:
        report = cls.evaluate(candidate, policy_id=policy_id)
        if report["decision"] != "PASS":
            raise AutoAcceptanceBlockedError(
                f"automatic candidate acceptance blocked; failed_gates={report['failed_gates']}"
            )
        return report


def build_portfolio(
    *,
    session_id: str,
    request_ref: Mapping[str, str],
    candidates: Sequence[CandidatePreviewCard],
) -> CandidatePortfolio:
    if not candidates:
        raise CandidateSelectionError("candidate portfolio cannot be empty")
    ids = [candidate.candidate_id for candidate in candidates]
    if len(ids) != len(set(ids)):
        raise CandidateSelectionError("candidate portfolio contains duplicate candidate IDs")
    ranks = [candidate.ranking for candidate in candidates]
    if len(ranks) != len(set(ranks)):
        raise CandidateSelectionError("candidate portfolio contains duplicate rankings")
    ordered = tuple(sorted(candidates, key=lambda item: (item.ranking, item.candidate_id)))
    core = {
        "portfolio_id": f"candidate-portfolio:{canonical_sha256({'session_id': session_id, 'request_ref': dict(request_ref), 'candidates': [c.model_dump(mode='json') for c in ordered]})[:24]}",
        "request_ref": dict(request_ref),
        "candidates": [candidate.model_dump(mode="json") for candidate in ordered],
    }
    return CandidatePortfolio(**core, portfolio_sha256=canonical_sha256(core))


def navigate_session(
    session: CandidatePreviewSession,
    portfolio: CandidatePortfolio,
    *,
    direction: NavigationDirection,
    expected_version: int,
) -> CandidatePreviewSession:
    _check_version(session, expected_version)
    count = len(portfolio.candidates)
    if count == 0:
        raise CandidateSelectionError("candidate portfolio cannot be empty")
    delta = 1 if direction == NavigationDirection.NEXT else -1
    next_index = (session.current_index + delta) % count
    current_id = portfolio.candidates[next_index].candidate_id
    seen = list(session.seen_candidate_ids)
    if current_id not in seen:
        seen.append(current_id)
    return session.model_copy(update={
        "current_index": next_index,
        "seen_candidate_ids": tuple(seen),
        "version": session.version + 1,
    })


def decide_session(
    session: CandidatePreviewSession,
    portfolio: CandidatePortfolio,
    *,
    candidate_id: str,
    decision: CandidateDecision,
    expected_version: int,
    operator_ref: Mapping[str, Any] | None = None,
    rationale: str | None = None,
    revision_ref: Mapping[str, str] | None = None,
    policy_id: str = POLICY_ID,
) -> tuple[CandidatePreviewSession, CandidateDecisionReceipt, dict[str, str]]:
    _check_version(session, expected_version)
    candidate = next((item for item in portfolio.candidates if item.candidate_id == candidate_id), None)
    if candidate is None:
        raise CandidateSelectionError(f"candidate '{candidate_id}' is not in the active portfolio")

    if decision in {CandidateDecision.ACCEPT, CandidateDecision.AUTO_ACCEPT} and candidate_id in session.rejected_candidate_ids:
        raise CandidateSelectionError(f"candidate '{candidate_id}' was already rejected in this session; search again is required before reconsideration")

    policy_report = AcceptancePolicyRegistry.evaluate(candidate, policy_id=policy_id)
    if decision == CandidateDecision.AUTO_ACCEPT:
        policy_report = AcceptancePolicyRegistry.assert_accept(candidate, policy_id=policy_id)
        receipt_operator = None
        policy_ref = policy_id
        effective_decision = CandidateDecision.AUTO_ACCEPT
    else:
        if not operator_ref or operator_ref.get("actor_type") != "human" or operator_ref.get("workflow_role") != "operator":
            raise CandidateSelectionError("manual candidate decisions require a human operator actor")
        if decision == CandidateDecision.REJECT and (not rationale or len(rationale.strip()) < 5):
            raise CandidateSelectionError("candidate rejection requires a rationale of at least 5 characters")
        receipt_operator = dict(operator_ref)
        policy_ref = None
        effective_decision = decision

    rejected = list(session.rejected_candidate_ids)
    if decision == CandidateDecision.REJECT and candidate_id not in rejected:
        rejected.append(candidate_id)

    new_status = "SELECTED" if decision in {CandidateDecision.ACCEPT, CandidateDecision.AUTO_ACCEPT} else session.status
    seen = list(session.seen_candidate_ids)
    if candidate_id not in seen:
        seen.append(candidate_id)
    next_session = session.model_copy(update={
        "selected_candidate_id": candidate_id if decision in {CandidateDecision.ACCEPT, CandidateDecision.AUTO_ACCEPT} else session.selected_candidate_id,
        "rejected_candidate_ids": tuple(rejected),
        "seen_candidate_ids": tuple(seen),
        "status": new_status,
        "version": session.version + 1,
    })
    selected_payload = candidate.model_dump(mode="json")
    rejected_payload = tuple(
        item.model_dump(mode="json") for item in portfolio.candidates if item.candidate_id in set(rejected)
    )
    receipt_core = {
        "mandate_id": MANDATE_ID,
        "session_id": session.session_id,
        "request_ref": dict(session.request_ref),
        "candidate_set_ref": {"object_id": portfolio.portfolio_id, "version": "1.0.0", "sha256": portfolio.portfolio_sha256},
        "selected_candidate": selected_payload,
        "rejected_candidates": list(rejected_payload),
        "operator_ref": receipt_operator,
        "auto_selection_policy": policy_ref,
        "source_ref": candidate.source_ref.model_dump(mode="json"),
        "source_hash": candidate.source_ref.sha256,
        "source_range": candidate.source_range_ms,
        "rights_state": candidate.rights_state,
        "storyboard_element_ref": dict(session.target_ref),
        "revision_ref": dict(revision_ref or {"object_id": session.target_ref["object_id"], "version": str(expected_version), "sha256": session.target_ref.get("sha256", "")}),
        "decision": effective_decision.value,
        "rationale": rationale,
    }
    receipt = CandidateDecisionReceipt(
        **receipt_core,
        receipt_id=f"candidate-decision:{canonical_sha256(receipt_core)[:24]}",
        receipt_sha256=canonical_sha256(receipt_core),
    )
    return next_session, receipt, policy_report


def _check_version(session: CandidatePreviewSession, expected_version: int) -> None:
    if expected_version != session.version:
        raise CandidateStaleVersionError(
            f"expected candidate session version {expected_version}, current {session.version}"
        )
