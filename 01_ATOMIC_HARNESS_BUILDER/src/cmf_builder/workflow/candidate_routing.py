"""Candidate race and human-governed compute routing contracts for ST-09.05."""

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


class CandidateRoutingError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CandidateAction(str, Enum):
    PLAN = "PLAN"
    SELECT = "SELECT"
    ROUTE = "ROUTE"
    INVALIDATE = "INVALIDATE"
    ROLLBACK = "ROLLBACK"


class AuthorityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


class GateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class HumanGateClass(str, Enum):
    CONSTITUTIONAL_DECISION = "constitutional_decision"
    PRODUCT_OR_POLICY_DECISION = "product_or_policy_decision"
    RISK_OR_BUDGET_ESCALATION = "risk_or_budget_escalation"
    WAIVER = "waiver"
    INCIDENT_AUTHORIZATION = "incident_authorization"
    RELEASE_OR_PROMOTION = "release_or_promotion"
    FINAL_REVIEW = "final_review_where_profile_requires_it"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CandidateRoutingError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _tuple(value: tuple[Any, ...], name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise CandidateRoutingError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class CandidateAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[CandidateAction, ...]
    applicable_scope: tuple[str, ...]
    status: AuthorityStatus = AuthorityStatus.ACTIVE

    def __post_init__(self) -> None:
        _text(self.authority_id, "authority_id")
        _text(self.authority_version, "authority_version")
        _text(self.authority_sha256, "authority_sha256")
        _tuple(self.permitted_actions, "permitted_actions")
        _tuple(self.applicable_scope, "applicable_scope")

    @property
    def authority_identity(self) -> str:
        return sha256_of(
            {
                "authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_sha256": self.authority_sha256,
                "permitted_actions": [action.value for action in self.permitted_actions],
                "applicable_scope": list(self.applicable_scope),
                "status": self.status.value,
            }
        )


@dataclass(frozen=True)
class CandidateCommand:
    command_id: str
    action: CandidateAction
    resource_id: str
    payload_sha256: str
    expected_authority_identity: str

    @property
    def command_identity(self) -> str:
        return sha256_of(
            {
                "command_id": self.command_id,
                "action": self.action.value,
                "resource_id": self.resource_id,
                "payload_sha256": self.payload_sha256,
                "expected_authority_identity": self.expected_authority_identity,
            }
        )


@dataclass(frozen=True)
class CandidateDeclaration:
    candidate_id: str
    canonical_output_sha256: str
    input_contract_hash: str
    output_contract_hash: str
    lineage_hash: str
    sandbox_policy_ref: str

    def __post_init__(self) -> None:
        for value, name in self.__dict__.items():
            _text(value, name)

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class CandidateRacePlan:
    race_id: str
    race_version: str
    workflow_profile_ref: str
    node_identity: str
    common_input_contract_hash: str
    common_output_contract_hash: str
    candidates: tuple[CandidateDeclaration, ...]
    evaluator_policy_hash: str
    minimum_view_contract_hash: str
    quality_gate: str
    cost_gate: str
    latency_gate: str
    budget_limit: str
    fan_out_limit: int
    deterministic_tie_policy: str
    authority_identity: str
    generation_or_evaluation_executed: bool = False

    def __post_init__(self) -> None:
        if self.generation_or_evaluation_executed:
            raise CandidateRoutingError("CANDIDATE_EXECUTION_PROHIBITED", "race plan cannot execute candidates")
        if self.fan_out_limit <= 0 or self.fan_out_limit < len(self.candidates):
            raise CandidateRoutingError("INVALID_CANDIDATE_FAN_OUT_LIMIT", "fan-out must bound declared candidates")
        _tuple(self.candidates, "candidates")
        contract_pairs = {(c.input_contract_hash, c.output_contract_hash) for c in self.candidates}
        if contract_pairs != {(self.common_input_contract_hash, self.common_output_contract_hash)}:
            raise CandidateRoutingError("CANDIDATE_CONTRACT_MISMATCH", "all candidates must share the common contracts")
        if len({c.sandbox_policy_ref for c in self.candidates}) != len(self.candidates):
            raise CandidateRoutingError("CANDIDATE_SANDBOX_NOT_INDEPENDENT", "candidate sandbox refs must be independent")
        for value, name in (
            (self.race_id, "race_id"),
            (self.race_version, "race_version"),
            (self.workflow_profile_ref, "workflow_profile_ref"),
            (self.node_identity, "node_identity"),
            (self.evaluator_policy_hash, "evaluator_policy_hash"),
            (self.minimum_view_contract_hash, "minimum_view_contract_hash"),
            (self.quality_gate, "quality_gate"),
            (self.cost_gate, "cost_gate"),
            (self.latency_gate, "latency_gate"),
            (self.budget_limit, "budget_limit"),
            (self.deterministic_tie_policy, "deterministic_tie_policy"),
            (self.authority_identity, "authority_identity"),
        ):
            _text(value, name)

    def as_dict(self) -> dict[str, Any]:
        return {
            "race_id": self.race_id,
            "race_version": self.race_version,
            "workflow_profile_ref": self.workflow_profile_ref,
            "node_identity": self.node_identity,
            "common_input_contract_hash": self.common_input_contract_hash,
            "common_output_contract_hash": self.common_output_contract_hash,
            "candidates": [candidate.as_dict() for candidate in self.candidates],
            "evaluator_policy_hash": self.evaluator_policy_hash,
            "minimum_view_contract_hash": self.minimum_view_contract_hash,
            "quality_gate": self.quality_gate,
            "cost_gate": self.cost_gate,
            "latency_gate": self.latency_gate,
            "budget_limit": self.budget_limit,
            "fan_out_limit": self.fan_out_limit,
            "deterministic_tie_policy": self.deterministic_tie_policy,
            "authority_identity": self.authority_identity,
            "generation_or_evaluation_executed": False,
        }

    @property
    def race_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class CandidateEvaluation:
    candidate_id: str
    evaluator_policy_hash: str
    rubric_hash: str
    evidence_hashes: tuple[str, ...]
    quality_status: GateStatus
    contract_status: GateStatus
    cost_status: GateStatus
    latency_status: GateStatus
    score: int
    authority_ref: str

    def __post_init__(self) -> None:
        _text(self.candidate_id, "candidate_id")
        _text(self.evaluator_policy_hash, "evaluator_policy_hash")
        _text(self.rubric_hash, "rubric_hash")
        _tuple(self.evidence_hashes, "evidence_hashes")
        _text(self.authority_ref, "authority_ref")

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "evaluator_policy_hash": self.evaluator_policy_hash,
            "rubric_hash": self.rubric_hash,
            "evidence_hashes": list(self.evidence_hashes),
            "quality_status": self.quality_status.value,
            "contract_status": self.contract_status.value,
            "cost_status": self.cost_status.value,
            "latency_status": self.latency_status.value,
            "score": self.score,
            "authority_ref": self.authority_ref,
        }


@dataclass(frozen=True)
class CandidateSelectionReceipt:
    race_identity: str
    winner_candidate_id: str
    evaluation_identities: tuple[str, ...]
    selection_reason: str
    no_first_completion_shortcut: bool
    command_identity: str

    @property
    def receipt_identity(self) -> str:
        return sha256_of(
            {
                "race_identity": self.race_identity,
                "winner_candidate_id": self.winner_candidate_id,
                "evaluation_identities": list(self.evaluation_identities),
                "selection_reason": self.selection_reason,
                "no_first_completion_shortcut": self.no_first_completion_shortcut,
                "command_identity": self.command_identity,
            }
        )


def compute_selection_payload_sha256(plan: CandidateRacePlan, evaluations: tuple[CandidateEvaluation, ...]) -> str:
    return sha256_of({"plan": plan.as_dict(), "evaluations": [evaluation.as_dict() for evaluation in evaluations]})


def select_candidate(
    plan: CandidateRacePlan,
    evaluations: tuple[CandidateEvaluation, ...],
    command: CandidateCommand,
    authority: CandidateAuthority,
) -> CandidateSelectionReceipt:
    _check(command, authority, CandidateAction.SELECT, plan.race_identity, compute_selection_payload_sha256(plan, evaluations))
    expected_ids = {candidate.candidate_id for candidate in plan.candidates}
    by_candidate = {evaluation.candidate_id: evaluation for evaluation in evaluations}
    if set(by_candidate) != expected_ids:
        raise CandidateRoutingError("MISSING_REQUIRED_EVALUATION", "all candidate evaluations are required")
    for evaluation in evaluations:
        if evaluation.evaluator_policy_hash != plan.evaluator_policy_hash:
            raise CandidateRoutingError("EVALUATOR_POLICY_MISMATCH", "evaluation policy mismatch")
        if GateStatus.FAIL in (evaluation.quality_status, evaluation.contract_status, evaluation.cost_status, evaluation.latency_status):
            raise CandidateRoutingError("CANDIDATE_GATE_FAILED", "winner cannot be selected when any gate fails")
    ordered = sorted(evaluations, key=lambda item: (-item.score, item.candidate_id))
    winner = ordered[0]
    return CandidateSelectionReceipt(
        plan.race_identity,
        winner.candidate_id,
        tuple(sha256_of(evaluation.as_dict()) for evaluation in sorted(evaluations, key=lambda item: item.candidate_id)),
        "highest deterministic score after all required gates passed",
        True,
        command.command_identity,
    )


@dataclass(frozen=True)
class ComputeRouteRequest:
    node_responsibility: str
    actor_kind: str
    task_complexity: int
    ambiguity: int
    risk: int
    expected_value: int
    prior_evidence_refs: tuple[str, ...]
    latency_budget: str
    cost_budget: str

    def __post_init__(self) -> None:
        for value, name in ((self.node_responsibility, "node_responsibility"), (self.actor_kind, "actor_kind"), (self.latency_budget, "latency_budget"), (self.cost_budget, "cost_budget")):
            _text(value, name)
        _tuple(self.prior_evidence_refs, "prior_evidence_refs")


@dataclass(frozen=True)
class ComputeRoutePolicy:
    policy_id: str
    registered_model_tiers: tuple[str, ...]
    registered_evaluator_strengths: tuple[str, ...]
    allowed_tool_grants: tuple[str, ...]
    max_candidate_count: int
    human_gate_threshold: int

    def __post_init__(self) -> None:
        _text(self.policy_id, "policy_id")
        _tuple(self.registered_model_tiers, "registered_model_tiers")
        _tuple(self.registered_evaluator_strengths, "registered_evaluator_strengths")
        if self.max_candidate_count <= 0:
            raise CandidateRoutingError("UNBOUNDED_ROUTE_FAN_OUT", "max candidate count required")

    @property
    def policy_identity(self) -> str:
        return sha256_of(self.__dict__)


@dataclass(frozen=True)
class ComputeRouteDecision:
    request_identity: str
    policy_identity: str
    abstract_model_tier: str
    candidate_count: int
    evaluator_strength: str
    tool_grants: tuple[str, ...]
    compute_budget: str
    required_human_gate_refs: tuple[str, ...]
    justification: str
    provider_or_model_selected: bool = False

    @property
    def decision_identity(self) -> str:
        return sha256_of(self.__dict__)


def route_compute(request: ComputeRouteRequest, policy: ComputeRoutePolicy) -> ComputeRouteDecision:
    pressure = request.task_complexity + request.ambiguity + request.risk
    if not request.prior_evidence_refs:
        raise CandidateRoutingError("MISSING_ROUTE_EVIDENCE", "prior evidence is required")
    tier = policy.registered_model_tiers[min(len(policy.registered_model_tiers) - 1, pressure // 7)]
    strength = policy.registered_evaluator_strengths[min(len(policy.registered_evaluator_strengths) - 1, max(0, pressure - 1) // 8)]
    count = min(policy.max_candidate_count, 1 + pressure // 8)
    human_gates = ("gate:risk-or-budget",) if request.risk >= policy.human_gate_threshold else ()
    return ComputeRouteDecision(
        sha256_of(request.__dict__),
        policy.policy_identity,
        tier,
        count,
        strength,
        tuple(tool for tool in policy.allowed_tool_grants if tool == "DEFAULT_DENY"),
        request.cost_budget,
        human_gates,
        "deterministic risk-aware abstract route; no provider, model, credential or network selected",
        False,
    )


@dataclass(frozen=True)
class EvaluatorView:
    candidate_identity: str
    canonical_output_sha256: str
    input_contract_hash: str
    rubric_hash: str
    evidence_hashes: tuple[str, ...]
    source_lineage_refs: tuple[str, ...]
    cost_latency_observations: tuple[str, ...]
    generator_hidden_reasoning: str = ""
    generator_preferred_answer: str = ""
    protected_benchmark_labels: tuple[str, ...] = ()
    credential_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.generator_hidden_reasoning or self.generator_preferred_answer or self.protected_benchmark_labels or self.credential_values:
            raise CandidateRoutingError("EVALUATOR_FORBIDDEN_VIEW", "evaluator view contains prohibited context")
        for value, name in ((self.candidate_identity, "candidate_identity"), (self.canonical_output_sha256, "canonical_output_sha256"), (self.input_contract_hash, "input_contract_hash"), (self.rubric_hash, "rubric_hash")):
            _text(value, name)
        _tuple(self.evidence_hashes, "evidence_hashes")
        _tuple(self.source_lineage_refs, "source_lineage_refs")

    @property
    def view_identity(self) -> str:
        return sha256_of(self.__dict__)


@dataclass(frozen=True)
class HumanGatePlacement:
    gate_id: str
    gate_class: HumanGateClass
    authority_required: str
    active: bool = True
    resolved_by_model_agent_or_policy: bool = False

    def __post_init__(self) -> None:
        _text(self.gate_id, "gate_id")
        _text(self.authority_required, "authority_required")
        if self.resolved_by_model_agent_or_policy:
            raise CandidateRoutingError("HUMAN_GATE_AUTOMATION_PROHIBITED", "human-owned gate cannot be resolved by automation")

    @property
    def gate_identity(self) -> str:
        return sha256_of({"gate_id": self.gate_id, "gate_class": self.gate_class.value, "authority_required": self.authority_required, "active": self.active})


@dataclass(frozen=True)
class CandidateTransitionReceipt:
    action: CandidateAction
    prior_identity: str
    active_after: bool
    historical_receipt_preserved: bool
    command_identity: str
    authority_identity: str

    @property
    def transition_identity(self) -> str:
        return sha256_of(self.__dict__ | {"action": self.action.value})


def compute_transition_payload_sha256(prior_identity: str, action: CandidateAction) -> str:
    return sha256_of({"prior_identity": prior_identity, "action": action.value})


def invalidate_candidate_decision(prior_identity: str, command: CandidateCommand, authority: CandidateAuthority) -> CandidateTransitionReceipt:
    _check(command, authority, CandidateAction.INVALIDATE, prior_identity, compute_transition_payload_sha256(prior_identity, CandidateAction.INVALIDATE))
    return CandidateTransitionReceipt(CandidateAction.INVALIDATE, prior_identity, False, True, command.command_identity, authority.authority_identity)


def rollback_candidate_decision(prior_identity: str, command: CandidateCommand, authority: CandidateAuthority) -> CandidateTransitionReceipt:
    _check(command, authority, CandidateAction.ROLLBACK, prior_identity, compute_transition_payload_sha256(prior_identity, CandidateAction.ROLLBACK))
    return CandidateTransitionReceipt(CandidateAction.ROLLBACK, prior_identity, False, True, command.command_identity, authority.authority_identity)


def validate_repeat_decision(existing_identity: str, repeated_identity: str) -> str:
    if existing_identity != repeated_identity:
        raise CandidateRoutingError("CONFLICTING_REPEAT_COMMAND", "decision payload differs")
    return existing_identity


def _check(command: CandidateCommand, authority: CandidateAuthority, action: CandidateAction, resource_id: str, payload_sha256: str) -> None:
    if authority.status is not AuthorityStatus.ACTIVE:
        raise CandidateRoutingError("INACTIVE_AUTHORITY", "authority inactive")
    if action not in authority.permitted_actions or command.action is not action:
        raise CandidateRoutingError("UNAUTHORIZED_ACTION", "action not permitted")
    if resource_id not in authority.applicable_scope and "*" not in authority.applicable_scope:
        raise CandidateRoutingError("AUTHORITY_SCOPE_MISMATCH", "resource outside authority")
    if command.resource_id != resource_id:
        raise CandidateRoutingError("COMMAND_RESOURCE_MISMATCH", "resource mismatch")
    if command.payload_sha256 != payload_sha256:
        raise CandidateRoutingError("COMMAND_PAYLOAD_MISMATCH", "payload mismatch")
    if command.expected_authority_identity != authority.authority_identity:
        raise CandidateRoutingError("AUTHORITY_IDENTITY_MISMATCH", "authority mismatch")
