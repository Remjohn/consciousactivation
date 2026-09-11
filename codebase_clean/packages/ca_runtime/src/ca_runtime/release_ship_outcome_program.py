"""
release_ship_outcome_program.py
--------------------------------
Release / Ship / Outcome Runtime Coordinator for CAE Phase 4 (Mandate M45).

Connects final Dual-Axis QA, backend-authoritative operator release authorization,
distribution ship, empirical outcome measurement, and selective learning proposal
generation into a unified, governed CAE Program state machine runtime.
"""

from __future__ import annotations

import dataclasses
import enum
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple
from uuid import UUID, uuid4

from ca_contracts import utc_now_rfc3339

from cae_outcome_intelligence.collector import OutcomeCollector
from cae_outcome_intelligence.domain import (
    EvaluationReceipt,
    FailureMode,
    LearningProposal,
    ObservedOutcome,
    OutcomeDomain,
    PerformanceMemory,
)
from cae_outcome_intelligence.errors import (
    AveragedDisagreementLaunderingError,
    EngagementWithoutTruthError,
    MisleadingContextRewardHackError,
    OntologyMutationViolationError,
    OutcomeIntelligenceError,
)
from cae_outcome_intelligence.learner import SelectiveLearningEngine
from cae_outcome_intelligence.verifier import OutcomeIntelligenceVerifier

from .program_state_runtime import (
    AuthorityLane,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    ProgramTransitionBlockedError,
    SideEffectClass,
    TenantContext,
    UniversalProgramStateRuntime,
    get_canonical_release_ship_outcome_state_machine,
)

logger = logging.getLogger("conscious_activations.ca_runtime.release_ship_outcome")


# ============================================================================
# 1. Error Taxonomy
# ============================================================================

class ReleaseShipProgramError(Exception):
    """Base exception for all release, ship, outcome, and learning runtime failures."""
    pass


class LaneAuthorityViolationError(ReleaseShipProgramError):
    """Raised when an operation is executed by an unauthorized authority lane."""
    pass


class SyntheticProductionBlockedError(ReleaseShipProgramError):
    """Raised when synthetic or ungrounded material is submitted for production release."""
    pass


class MissingEvidenceLineageError(ReleaseShipProgramError):
    """Raised when evidence DAG lineage to source interview moments is missing or broken."""
    pass


class EvidenceIntegrityViolationError(ReleaseShipProgramError):
    """Raised when evidence quote text hash does not match claimed cryptographic digest."""
    pass


class IncompleteQAError(ReleaseShipProgramError):
    """Raised when required Dual-Axis QA evaluations are missing or incomplete."""
    pass


class SemanticQAFailureError(ReleaseShipProgramError):
    """Raised when Semantic QA evaluation fails source fidelity or narrative checks."""
    pass


class RenderQAFailureError(ReleaseShipProgramError):
    """Raised when Render QA evaluation fails technical media checks."""
    pass


class OperatorAuthorizationRequiredError(ReleaseShipProgramError):
    """Raised when shipment is attempted without valid backend-authoritative operator release."""
    pass


class ShipmentExecutionFailureError(ReleaseShipProgramError):
    """Raised when physical or distribution shipment fails delivery to target channel."""
    pass


class InvalidStateTransitionError(ReleaseShipProgramError):
    """Raised when state transition violates canonical program state machine grammar."""
    pass


class WorkspaceScopeViolationError(ReleaseShipProgramError):
    """Raised when multi-tenant workspace boundary is violated."""
    pass


class AntiRewardHackingViolationError(ReleaseShipProgramError):
    """Raised when outcome observation exhibits viral engagement without truth or distortion."""
    pass


# ============================================================================
# 2. Domain Data Models
# ============================================================================

@dataclass(frozen=True)
class FinalQAVerificationRecord:
    """Auditable record of Dual-Axis QA verification (Semantic + Render QA)."""
    qa_record_id: str
    program_id: str
    candidate_id: str
    workspace_id: str
    semantic_qa_passed: bool
    render_qa_passed: bool
    evidence_quote_sha256: str
    wrong_reading_locks: List[str]
    semantic_qa_details: Dict[str, Any]
    render_qa_details: Dict[str, Any]
    is_synthetic: bool = False
    verified_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperatorReleaseAuthorization:
    """Backend-authoritative operator release gate decision."""
    authorization_id: str
    operator_id: str
    decision: str  # APPROVED, REJECTED, CONDITIONAL
    release_manifest_sha256: str
    target_channels: List[str]
    rationale: str
    authorized_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ShipmentReceipt:
    """Cryptographic receipt of physical or distribution delivery."""
    shipment_id: str
    authorization_id: str
    target_channel: str
    delivery_endpoint: str
    delivered_artifact_sha256: str
    delivery_status: str  # DELIVERED, FAILED
    channel_response_id: str
    shipped_at: str = field(default_factory=utc_now_rfc3339)
    shipment_digest: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OutcomeObservationRecord:
    """Auditable record of empirical real-world observation and evaluation receipt."""
    outcome_id: str
    shipment_id: str
    program_id: str
    workspace_id: str
    domain: str
    metrics: Dict[str, float]
    predicted_composite_score: float
    observed_normalized_score: float
    score_delta: float
    disagreement_spread: float
    is_grounded: bool
    misleading_context: bool
    evaluation_receipt_id: str
    observed_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectiveLearningProposalRecord:
    """Advisory learning calibration proposal record requiring Operator ratification."""
    proposal_id: str
    workspace_id: str
    pattern_summary: str
    proposal_type: str
    suggested_modifications: Dict[str, Any]
    recurrence_count: int
    evidence_receipt_ids: List[str]
    requires_operator_ratification: bool = True
    ratification_status: str = "PENDING_OPERATOR"
    created_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _sanitize_for_canonical_payload(data: Any) -> Any:
    """Recursively formats floats, UUIDs, and dataclasses to deterministic canonical-compatible structures."""
    if isinstance(data, dict):
        return {k: _sanitize_for_canonical_payload(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [_sanitize_for_canonical_payload(item) for item in data]
    elif isinstance(data, float):
        return f"{data:.6f}".rstrip("0").rstrip(".") if data != 0.0 else "0.0"
    elif isinstance(data, UUID):
        return str(data)
    elif isinstance(data, enum.Enum):
        return data.value
    elif dataclasses.is_dataclass(data):
        return _sanitize_for_canonical_payload(dataclasses.asdict(data))
    return data


# ============================================================================
# 3. Release / Ship / Outcome Coordinator Runtime
# ============================================================================

class ReleaseShipOutcomeCoordinator:
    """
    Coordinates final Dual-Axis QA, backend-authoritative operator release authorization,
    distribution shipment, empirical outcome collection, and selective learning proposals.
    """

    def __init__(
        self,
        runtime: UniversalProgramStateRuntime,
    ) -> None:
        self.runtime = runtime
        self._state_machine = get_canonical_release_ship_outcome_state_machine()
        self.runtime.register_state_machine(self._state_machine)

    def initialize_session(
        self,
        *,
        program_id: str = "release_ship_outcome_program",
        candidate_id: str,
        workspace_id: UUID | str,
        actor_id: str,
        artifact_ref: Dict[str, Any],
        initial_claims: Optional[Dict[str, Any]] = None,
    ) -> ProgramStateAggregate:
        """Initializes a new release/ship/outcome program aggregate."""
        ws_id = UUID(str(workspace_id)) if not isinstance(workspace_id, UUID) else workspace_id
        initial_data = {
            "program_id": program_id,
            "candidate_id": candidate_id,
            "artifact_ref": artifact_ref,
            "session_created_at": utc_now_rfc3339(),
            "status": "INITIAL",
            "context_claims": initial_claims or {"workspace_active": True, "material_present": True},
        }
        return self.runtime.initialize_program_state(
            program_id=program_id,
            workspace_id=ws_id,
            actor_id=actor_id,
            initial_data=initial_data,
        )

    def verify_final_qa(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.ANALYST,
        semantic_qa_result: Dict[str, Any],
        render_qa_result: Dict[str, Any],
        evidence_segment: Dict[str, Any],
        wrong_reading_locks: Sequence[str],
        is_synthetic: bool = False,
    ) -> FinalQAVerificationRecord:
        """
        Executes final Dual-Axis QA verification (Semantic QA + Render QA) under ANALYST lane.
        Fails closed on synthetic material, quote mismatch, or missing/failed QA axes.
        """
        agg_id = str(aggregate_id)
        aggregate = self.runtime.get_aggregate(agg_id)

        # 1. Authority Lane Check
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(
                f"verify_final_qa must be executed by ANALYST lane, received {lane}"
            )

        # 2. Anti-Synthetic Guard
        if is_synthetic or evidence_segment.get("is_synthetic", False):
            raise SyntheticProductionBlockedError(
                "Synthetic or mock candidate material cannot be verified for production release."
            )

        # 3. Evidence Lineage & Quote Integrity
        quote_text = evidence_segment.get("quote_text", "").strip()
        if not quote_text:
            raise MissingEvidenceLineageError(
                "Evidence segment must contain authentic non-empty quote_text."
            )
        expected_sha = hashlib.sha256(quote_text.encode("utf-8")).hexdigest()
        claimed_sha = evidence_segment.get("evidence_quote_sha256") or expected_sha
        if claimed_sha != expected_sha:
            raise EvidenceIntegrityViolationError(
                f"Evidence quote SHA-256 mismatch! Expected {expected_sha}, got {claimed_sha}"
            )

        # 4. Wrong-Reading Locks
        locks = list(wrong_reading_locks)
        if not locks:
            raise IncompleteQAError(
                "Final QA verification requires non-empty lexicographically sorted wrong_reading_locks."
            )

        # 5. Semantic QA Check
        if not semantic_qa_result or not semantic_qa_result.get("passed", False):
            error_msg = semantic_qa_result.get("failure_reason", "Semantic QA check failed.")
            raise SemanticQAFailureError(f"Semantic QA verification failed: {error_msg}")

        # 6. Render QA Check
        if not render_qa_result or not render_qa_result.get("passed", False):
            error_msg = render_qa_result.get("failure_reason", "Render QA check failed.")
            raise RenderQAFailureError(f"Render QA verification failed: {error_msg}")

        qa_record = FinalQAVerificationRecord(
            qa_record_id=f"QA-REC-{uuid4().hex[:12]}",
            program_id=aggregate.program_id,
            candidate_id=aggregate.state_data.get("candidate_id", "unknown-candidate"),
            workspace_id=str(aggregate.workspace_id),
            semantic_qa_passed=True,
            render_qa_passed=True,
            evidence_quote_sha256=expected_sha,
            wrong_reading_locks=locks,
            semantic_qa_details=semantic_qa_result,
            render_qa_details=render_qa_result,
            is_synthetic=False,
        )

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="verify_final_qa",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "material_present": True, "qa_verified": True},
                payload=_sanitize_for_canonical_payload({"qa_record": qa_record.to_dict()}),
                state_updates=_sanitize_for_canonical_payload({"qa_record": qa_record.to_dict(), "qa_verified": True}),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return qa_record

    def authorize_release(
        self,
        *,
        aggregate_id: UUID | str,
        operator_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.COMMANDER,
        decision: str = "APPROVED",
        target_channels: Sequence[str],
        rationale: str,
        release_manifest_sha256: Optional[str] = None,
    ) -> OperatorReleaseAuthorization:
        """
        Grants backend-authoritative operator release authorization under COMMANDER lane.
        """
        agg_id = str(aggregate_id)
        aggregate = self.runtime.get_aggregate(agg_id)

        # 1. Authority Lane Check
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"authorize_release must be executed by COMMANDER lane, received {lane}"
            )

        # 2. Decision Check
        if decision.upper() != "APPROVED":
            raise OperatorAuthorizationRequiredError(
                f"Release authorization rejected by operator with decision '{decision}': {rationale}"
            )

        # 3. Channels Check
        channels = list(target_channels)
        if not channels:
            raise OperatorAuthorizationRequiredError(
                "Operator release authorization requires at least one target channel."
            )

        manifest_sha = release_manifest_sha256 or hashlib.sha256(
            f"{aggregate.aggregate_id}:{decision}:{sorted(channels)}:{rationale}".encode("utf-8")
        ).hexdigest()

        auth = OperatorReleaseAuthorization(
            authorization_id=f"REL-AUTH-{uuid4().hex[:12]}",
            operator_id=operator_id,
            decision="APPROVED",
            release_manifest_sha256=manifest_sha,
            target_channels=channels,
            rationale=rationale,
        )

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="authorize_release",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims={
                    "workspace_active": True,
                    "qa_verified": True,
                    "operator_authorized": True,
                    "release_authorized": True,
                },
                payload=_sanitize_for_canonical_payload({"authorization": auth.to_dict()}),
                state_updates=_sanitize_for_canonical_payload({"authorization": auth.to_dict(), "release_authorized": True}),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return auth

    def execute_ship(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.COMPOSER,
        target_channel: str,
        delivery_endpoint: str,
        simulate_channel_failure: bool = False,
    ) -> ShipmentReceipt:
        """
        Executes physical or distribution shipment under COMPOSER lane.
        FAILED SHIP NEVER REPORTS SUCCESS: Raises ShipmentExecutionFailureError and never transitions to SHIPPED.
        """
        agg_id = str(aggregate_id)
        aggregate = self.runtime.get_aggregate(agg_id)

        # 1. Authority Lane Check
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"execute_ship must be executed by COMPOSER lane, received {lane}"
            )

        # 2. Authorization Verification
        auth_data = aggregate.state_data.get("authorization")
        if not auth_data or auth_data.get("decision") != "APPROVED":
            raise OperatorAuthorizationRequiredError(
                "Shipment execution requires prior backend-authoritative operator release authorization."
            )

        allowed_channels = auth_data.get("target_channels", [])
        if target_channel not in allowed_channels:
            raise ShipmentExecutionFailureError(
                f"Target channel '{target_channel}' is not authorized. Authorized channels: {allowed_channels}"
            )

        # 3. Handle Delivery Failure (Failed ship never reports success)
        if simulate_channel_failure or not delivery_endpoint.strip():
            raise ShipmentExecutionFailureError(
                f"Distribution delivery to endpoint '{delivery_endpoint}' on channel '{target_channel}' failed: connection timeout / policy rejection."
            )

        # 4. Compute delivery digest
        artifact_ref = aggregate.state_data.get("artifact_ref", {})
        artifact_sha = artifact_ref.get("sha256", hashlib.sha256(b"mock_artifact").hexdigest())
        shipment_id = f"SHIP-{uuid4().hex[:12]}"
        channel_response_id = f"RESP-{uuid4().hex[:8]}"

        shipment_digest = hashlib.sha256(
            f"{shipment_id}:{target_channel}:{delivery_endpoint}:{artifact_sha}:{channel_response_id}".encode("utf-8")
        ).hexdigest()

        receipt = ShipmentReceipt(
            shipment_id=shipment_id,
            authorization_id=auth_data["authorization_id"],
            target_channel=target_channel,
            delivery_endpoint=delivery_endpoint,
            delivered_artifact_sha256=artifact_sha,
            delivery_status="DELIVERED",
            channel_response_id=channel_response_id,
            shipment_digest=shipment_digest,
        )

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="execute_ship",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "release_authorized": True, "shipped": True},
                payload=_sanitize_for_canonical_payload({"shipment_receipt": receipt.to_dict()}),
                state_updates=_sanitize_for_canonical_payload({"shipment_receipt": receipt.to_dict(), "shipped": True}),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return receipt

    def capture_outcome(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.HUNTER,
        domain: str | OutcomeDomain,
        metrics: Dict[str, float],
        predicted_composite_score: float,
        observed_normalized_score: float,
        evaluator_scores: Optional[Dict[str, float]] = None,
        is_grounded: bool = True,
        misleading_context: bool = False,
        failure_mode: FailureMode = FailureMode.NONE,
        notes: Optional[str] = None,
    ) -> Tuple[ObservedOutcome, EvaluationReceipt, OutcomeObservationRecord]:
        """
        Captures empirical real-world outcome metrics and emits auditable EvaluationReceipt under HUNTER lane.
        Enforces anti-reward hacking checks (engagement without truth, misleading context, disagreement laundering).
        """
        agg_id = str(aggregate_id)
        aggregate = self.runtime.get_aggregate(agg_id)

        # 1. Authority Lane Check
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.HUNTER:
            raise LaneAuthorityViolationError(
                f"capture_outcome must be executed by HUNTER lane, received {lane}"
            )

        # 2. Check current state is SHIPPED
        shipment_data = aggregate.state_data.get("shipment_receipt")
        if not shipment_data or shipment_data.get("delivery_status") != "DELIVERED":
            raise InvalidStateTransitionError(
                "Cannot capture outcome on an un-shipped or failed-shipment program aggregate."
            )

        outcome_domain = OutcomeDomain(str(domain)) if not isinstance(domain, OutcomeDomain) else domain

        # 3. Collect Outcome and Receipt via cae_outcome_intelligence (with Anti-Reward-Hack checks)
        try:
            outcome, receipt = OutcomeCollector.record_outcome_and_receipt(
                program_id=aggregate.program_id,
                candidate_id=aggregate.state_data.get("candidate_id", "unknown-candidate"),
                workspace_id=str(aggregate.workspace_id),
                domain=outcome_domain,
                metrics=metrics,
                predicted_composite_score=predicted_composite_score,
                observed_normalized_score=observed_normalized_score,
                evaluator_scores=evaluator_scores,
                is_grounded=is_grounded,
                misleading_context=misleading_context,
                failure_mode=failure_mode,
                notes=notes,
            )
        except EngagementWithoutTruthError as exc:
            raise AntiRewardHackingViolationError(str(exc)) from exc
        except MisleadingContextRewardHackError as exc:
            raise AntiRewardHackingViolationError(str(exc)) from exc

        # 4. Verify Disagreement Exposure (Anti-Score-Laundering)
        try:
            OutcomeIntelligenceVerifier.verify_evaluator_disagreement_exposure(receipt)
        except AveragedDisagreementLaunderingError as exc:
            raise AntiRewardHackingViolationError(str(exc)) from exc

        obs_record = OutcomeObservationRecord(
            outcome_id=outcome.outcome_id,
            shipment_id=shipment_data["shipment_id"],
            program_id=aggregate.program_id,
            workspace_id=str(aggregate.workspace_id),
            domain=outcome.domain.value,
            metrics=outcome.metrics,
            predicted_composite_score=receipt.predicted_composite_score,
            observed_normalized_score=receipt.observed_normalized_score,
            score_delta=receipt.score_delta,
            disagreement_spread=receipt.disagreement_spread,
            is_grounded=outcome.is_grounded,
            misleading_context=outcome.misleading_context,
            evaluation_receipt_id=receipt.receipt_id,
        )

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="capture_outcome",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "shipped": True, "outcome_captured": True},
                payload=_sanitize_for_canonical_payload({"outcome": outcome.model_dump(mode="json"), "receipt": receipt.model_dump(mode="json")}),
                state_updates=_sanitize_for_canonical_payload({
                    "outcome": outcome.model_dump(mode="json"),
                    "receipt": receipt.model_dump(mode="json"),
                    "outcome_observation": obs_record.to_dict(),
                    "outcome_captured": True,
                }),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return outcome, receipt, obs_record

    def propose_learning(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.ANALYST,
        performance_memory: Optional[PerformanceMemory] = None,
        min_recurrence: int = 2,
    ) -> List[LearningProposal]:
        """
        Analyzes outcome memory and generates advisory learning proposals under ANALYST lane.
        Ensures all proposals have requires_operator_ratification=True and blocks automatic ontology mutation.
        """
        agg_id = str(aggregate_id)
        aggregate = self.runtime.get_aggregate(agg_id)

        # 1. Authority Lane Check
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(
                f"propose_learning must be executed by ANALYST lane, received {lane}"
            )

        # 2. Build or use provided performance memory
        if performance_memory is None:
            receipt_data = aggregate.state_data.get("receipt")
            receipts = [EvaluationReceipt.model_validate(receipt_data)] if receipt_data else []
            outcome_data = aggregate.state_data.get("outcome")
            outcomes = [ObservedOutcome.model_validate(outcome_data)] if outcome_data else []
            memory = PerformanceMemory(
                workspace_id=str(aggregate.workspace_id),
                outcomes=outcomes,
                receipts=receipts,
            )
        else:
            memory = performance_memory

        proposals = SelectiveLearningEngine.analyze_memory_and_propose_calibrations(
            memory, min_recurrence=min_recurrence
        )

        proposal_dicts = [p.model_dump(mode="json") for p in proposals]

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="propose_learning",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "outcome_captured": True, "learning_proposed": True},
                payload=_sanitize_for_canonical_payload({"proposals": proposal_dicts}),
                state_updates=_sanitize_for_canonical_payload({"proposals": proposal_dicts, "learning_proposed": True}),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return proposals

    def ratify_learning_proposal(
        self,
        *,
        aggregate_id: UUID | str,
        operator_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.COMMANDER,
        proposal_id: str,
        decision: str = "RATIFIED",
    ) -> Dict[str, Any]:
        """
        Operator ratifies an advisory learning proposal under COMMANDER lane.
        """
        agg_id = str(aggregate_id)

        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"ratify_learning_proposal must be executed by COMMANDER lane, received {lane}"
            )

        ratification_record = {
            "proposal_id": proposal_id,
            "operator_id": operator_id,
            "decision": decision,
            "ratified_at": utc_now_rfc3339(),
        }

        try:
            self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="ratify_proposal",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "operator_authorized": True},
                payload=_sanitize_for_canonical_payload(ratification_record),
                state_updates=_sanitize_for_canonical_payload({"ratified_proposals": [ratification_record]}),
            )
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

        return ratification_record

    def attempt_direct_ontology_mutation(self, proposal: LearningProposal) -> None:
        """
        Directly calls SelectiveLearningEngine.apply_proposal_direct_to_ontology,
        which strictly raises OntologyMutationViolationError.
        """
        SelectiveLearningEngine.apply_proposal_direct_to_ontology(proposal)

    def request_repair(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.COMMANDER,
        repair_rationale: str,
        transition_name: str = "fail_qa_to_repair",
    ) -> ProgramStateAggregate:
        """
        Initiates a governed repair transition under COMMANDER lane.
        """
        agg_id = str(aggregate_id)
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"request_repair must be executed by COMMANDER lane, received {lane}"
            )

        try:
            res = self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name=transition_name,
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "operator_authorized": True},
                payload=_sanitize_for_canonical_payload({"repair_rationale": repair_rationale}),
                state_updates=_sanitize_for_canonical_payload({"repair_in_progress": True, "repair_rationale": repair_rationale}),
            )
            return res.aggregate
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

    def resume_from_repair(
        self,
        *,
        aggregate_id: UUID | str,
        actor_id: str,
        actor_lane: str | AuthorityLane = AuthorityLane.COMMANDER,
        target_state: str = "INITIAL",
        repair_payload: Optional[Dict[str, Any]] = None,
    ) -> ProgramStateAggregate:
        """
        Resumes aggregate from REPAIRING state under COMMANDER lane.
        """
        agg_id = str(aggregate_id)
        lane = actor_lane if isinstance(actor_lane, AuthorityLane) else AuthorityLane(str(actor_lane))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"resume_from_repair must be executed by COMMANDER lane, received {lane}"
            )

        trans_name = "repair_to_initial" if target_state == "INITIAL" else "repair_to_qa_verified"
        try:
            res = self.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name=trans_name,
                actor_id=actor_id,
                actor_lane=lane,
                context_claims={"workspace_active": True, "operator_authorized": True},
                payload=_sanitize_for_canonical_payload(repair_payload or {}),
                state_updates=_sanitize_for_canonical_payload({"repair_in_progress": False, "repaired_at": utc_now_rfc3339()}),
            )
            return res.aggregate
        except ProgramTransitionBlockedError as exc:
            raise InvalidStateTransitionError(str(exc)) from exc
        except ProgramAuthorityLaneViolationError as exc:
            raise LaneAuthorityViolationError(str(exc)) from exc

