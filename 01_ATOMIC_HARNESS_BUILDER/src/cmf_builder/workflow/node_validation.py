"""Node-output validation and localized failure containment for ST-09.03."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class NodeValidationError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class OutputDecision(str, Enum):
    RELEASE_VALIDATED = "RELEASE_VALIDATED"
    BLOCK_VALIDATION_FAILED = "BLOCK_VALIDATION_FAILED"


class OutputState(str, Enum):
    QUARANTINED_PENDING_VALIDATION = "QUARANTINED_PENDING_VALIDATION"
    RELEASED_VALIDATED = "RELEASED_VALIDATED"
    BLOCKED_VALIDATION_FAILED = "BLOCKED_VALIDATION_FAILED"
    INVALIDATED = "INVALIDATED"


class NodeValidationAction(str, Enum):
    VALIDATE = "VALIDATE"
    INVALIDATE = "INVALIDATE"
    ROLLBACK = "ROLLBACK"


class AuthorityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


def _required_text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise NodeValidationError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _non_empty_tuple(value: tuple[Any, ...], name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise NodeValidationError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class NodeOutputSnapshot:
    workflow_identity: str
    workflow_version: str
    node_identity: str
    node_version: str
    input_sha256: str
    output_sha256: str
    output_contract: str
    state: OutputState = OutputState.QUARANTINED_PENDING_VALIDATION
    active: bool = True
    invalidated: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.workflow_identity, "workflow_identity"),
            (self.workflow_version, "workflow_version"),
            (self.node_identity, "node_identity"),
            (self.node_version, "node_version"),
            (self.input_sha256, "input_sha256"),
            (self.output_sha256, "output_sha256"),
            (self.output_contract, "output_contract"),
        ):
            _required_text(value, name)

    def as_dict(self) -> dict[str, Any]:
        return {
            "workflow_identity": self.workflow_identity,
            "workflow_version": self.workflow_version,
            "node_identity": self.node_identity,
            "node_version": self.node_version,
            "input_sha256": self.input_sha256,
            "output_sha256": self.output_sha256,
            "output_contract": self.output_contract,
            "state": self.state.value,
            "active": self.active,
            "invalidated": self.invalidated,
        }

    @property
    def snapshot_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class ValidationCheck:
    check_id: str
    check_kind: str
    status: CheckStatus
    evidence_sha256: str
    authority_ref: str
    not_applicable_basis: str = ""
    active: bool = True
    invalidated: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.check_id, "check_id"),
            (self.check_kind, "check_kind"),
            (self.evidence_sha256, "evidence_sha256"),
            (self.authority_ref, "authority_ref"),
        ):
            _required_text(value, name)
        if self.status is CheckStatus.NOT_APPLICABLE:
            _required_text(self.not_applicable_basis, "not_applicable_basis")

    def as_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "check_kind": self.check_kind,
            "status": self.status.value,
            "evidence_sha256": self.evidence_sha256,
            "authority_ref": self.authority_ref,
            "not_applicable_basis": self.not_applicable_basis,
            "active": self.active,
            "invalidated": self.invalidated,
        }


@dataclass(frozen=True)
class NodeValidationPolicy:
    policy_id: str
    policy_version: str
    required_check_kinds: tuple[str, ...]
    semantic_evaluator_required: bool
    allow_not_applicable_semantic_evaluator: bool
    hard_gate_ids: tuple[str, ...]
    completion_criteria: tuple[str, ...]

    def __post_init__(self) -> None:
        _required_text(self.policy_id, "policy_id")
        _required_text(self.policy_version, "policy_version")
        _non_empty_tuple(self.required_check_kinds, "required_check_kinds")
        _non_empty_tuple(self.hard_gate_ids, "hard_gate_ids")
        _non_empty_tuple(self.completion_criteria, "completion_criteria")

    def as_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "required_check_kinds": list(self.required_check_kinds),
            "semantic_evaluator_required": self.semantic_evaluator_required,
            "allow_not_applicable_semantic_evaluator": self.allow_not_applicable_semantic_evaluator,
            "hard_gate_ids": list(self.hard_gate_ids),
            "completion_criteria": list(self.completion_criteria),
        }

    @property
    def policy_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class NodeValidationAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[NodeValidationAction, ...]
    applicable_nodes: tuple[str, ...]
    status: AuthorityStatus = AuthorityStatus.ACTIVE

    def __post_init__(self) -> None:
        _required_text(self.authority_id, "authority_id")
        _required_text(self.authority_version, "authority_version")
        _required_text(self.authority_sha256, "authority_sha256")
        _non_empty_tuple(self.permitted_actions, "permitted_actions")
        _non_empty_tuple(self.applicable_nodes, "applicable_nodes")

    @property
    def authority_identity(self) -> str:
        return sha256_of(
            {
                "authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_sha256": self.authority_sha256,
                "permitted_actions": [action.value for action in self.permitted_actions],
                "applicable_nodes": list(self.applicable_nodes),
                "status": self.status.value,
            }
        )


@dataclass(frozen=True)
class NodeValidationCommand:
    command_id: str
    action: NodeValidationAction
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
class NodeValidationReceipt:
    snapshot: NodeOutputSnapshot
    policy: NodeValidationPolicy
    checks: tuple[ValidationCheck, ...]
    authority_identity: str
    command_identity: str
    decision: OutputDecision
    release_state: OutputState
    downstream_scheduling_eligible: bool
    failure_code: str
    failure_context: str
    predecessor_receipts: tuple[str, ...]
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "snapshot": self.snapshot.as_dict(),
            "policy": self.policy.as_dict(),
            "checks": [check.as_dict() for check in self.checks],
            "authority_identity": self.authority_identity,
            "command_identity": self.command_identity,
            "decision": self.decision.value,
            "release_state": self.release_state.value,
            "downstream_scheduling_eligible": self.downstream_scheduling_eligible,
            "failure_code": self.failure_code,
            "failure_context": self.failure_context,
            "predecessor_receipts": list(self.predecessor_receipts),
            "production_ready": False,
            "certified": False,
        }

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        identity = sha256_of(payload)
        if identity != self._anchor:
            raise NodeValidationError("MUTATED_GOVERNED_OBJECT", "receipt changed after issue")
        payload["receipt_identity"] = identity
        return payload


def compute_node_validation_payload_sha256(
    snapshot: NodeOutputSnapshot,
    policy: NodeValidationPolicy,
    checks: tuple[ValidationCheck, ...],
    predecessor_receipts: tuple[str, ...],
) -> str:
    return sha256_of(
        {
            "snapshot": snapshot.as_dict(),
            "policy": policy.as_dict(),
            "checks": [check.as_dict() for check in checks],
            "predecessor_receipts": list(predecessor_receipts),
        }
    )


def validate_node_output(
    *,
    snapshot: NodeOutputSnapshot,
    policy: NodeValidationPolicy,
    checks: tuple[ValidationCheck, ...],
    authority: NodeValidationAuthority,
    command: NodeValidationCommand,
    predecessor_receipts: tuple[str, ...],
) -> NodeValidationReceipt:
    if snapshot.state is not OutputState.QUARANTINED_PENDING_VALIDATION:
        raise NodeValidationError("UNQUARANTINED_OUTPUT_RELEASE_PROHIBITED", "output must start quarantined")
    if not snapshot.active or snapshot.invalidated:
        raise NodeValidationError("INVALIDATED_OUTPUT", "invalidated output cannot advance")
    _check_command(
        command,
        authority,
        NodeValidationAction.VALIDATE,
        snapshot.snapshot_identity,
        compute_node_validation_payload_sha256(snapshot, policy, checks, predecessor_receipts),
    )

    by_kind: dict[str, ValidationCheck] = {}
    for check in checks:
        if check.check_kind in by_kind:
            raise NodeValidationError("DUPLICATE_VALIDATION_CHECK", "one check per kind")
        by_kind[check.check_kind] = check

    missing = [kind for kind in policy.required_check_kinds if kind not in by_kind]
    if missing:
        return _blocked(snapshot, policy, checks, authority, command, "MISSING_DECLARED_CHECK", ",".join(missing), predecessor_receipts)

    for check in checks:
        if not check.active or check.invalidated:
            return _blocked(snapshot, policy, checks, authority, command, "STALE_OR_INVALIDATED_CHECK", check.check_id, predecessor_receipts)
        if check.status is CheckStatus.FAIL:
            return _blocked(snapshot, policy, checks, authority, command, "VALIDATION_CHECK_FAILED", check.check_id, predecessor_receipts)
        if check.status is CheckStatus.NOT_APPLICABLE and check.check_kind != "semantic_evaluator":
            return _blocked(snapshot, policy, checks, authority, command, "UNSUPPORTED_NOT_APPLICABLE_CHECK", check.check_kind, predecessor_receipts)

    semantic = by_kind.get("semantic_evaluator")
    if policy.semantic_evaluator_required and semantic is None:
        return _blocked(snapshot, policy, checks, authority, command, "MISSING_SEMANTIC_EVALUATOR_RECEIPT", "semantic_evaluator", predecessor_receipts)
    if semantic and semantic.status is CheckStatus.NOT_APPLICABLE and not policy.allow_not_applicable_semantic_evaluator:
        return _blocked(snapshot, policy, checks, authority, command, "SEMANTIC_EVALUATOR_REQUIRED", semantic.check_id, predecessor_receipts)

    return NodeValidationReceipt(
        snapshot=snapshot,
        policy=policy,
        checks=tuple(sorted(checks, key=lambda check: check.check_kind)),
        authority_identity=authority.authority_identity,
        command_identity=command.command_identity,
        decision=OutputDecision.RELEASE_VALIDATED,
        release_state=OutputState.RELEASED_VALIDATED,
        downstream_scheduling_eligible=True,
        failure_code="",
        failure_context="",
        predecessor_receipts=tuple(predecessor_receipts),
    )


def _blocked(
    snapshot: NodeOutputSnapshot,
    policy: NodeValidationPolicy,
    checks: tuple[ValidationCheck, ...],
    authority: NodeValidationAuthority,
    command: NodeValidationCommand,
    code: str,
    context: str,
    predecessor_receipts: tuple[str, ...],
) -> NodeValidationReceipt:
    return NodeValidationReceipt(
        snapshot=snapshot,
        policy=policy,
        checks=tuple(sorted(checks, key=lambda check: check.check_kind)),
        authority_identity=authority.authority_identity,
        command_identity=command.command_identity,
        decision=OutputDecision.BLOCK_VALIDATION_FAILED,
        release_state=OutputState.BLOCKED_VALIDATION_FAILED,
        downstream_scheduling_eligible=False,
        failure_code=code,
        failure_context=context,
        predecessor_receipts=tuple(predecessor_receipts),
    )


@dataclass(frozen=True)
class FailureFeedbackPackage:
    validation_receipt_identity: str
    failed_node_identity: str
    failed_criterion: str
    reproduction_evidence_refs: tuple[str, ...]
    responsible_root_cause_owner: str
    repair_and_invalidation_graph_ref: str
    allowed_diagnosis_scope: tuple[str, ...]
    frozen_state_ref: str
    affected_descendant_refs: tuple[str, ...]
    targeted_regression_requirements: tuple[str, ...]
    escalation_conditions: tuple[str, ...]
    delivered_to_owner: str
    broadcast: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.validation_receipt_identity, "validation_receipt_identity"),
            (self.failed_node_identity, "failed_node_identity"),
            (self.failed_criterion, "failed_criterion"),
            (self.responsible_root_cause_owner, "responsible_root_cause_owner"),
            (self.repair_and_invalidation_graph_ref, "repair_and_invalidation_graph_ref"),
            (self.frozen_state_ref, "frozen_state_ref"),
            (self.delivered_to_owner, "delivered_to_owner"),
        ):
            _required_text(value, name)
        for value, name in (
            (self.reproduction_evidence_refs, "reproduction_evidence_refs"),
            (self.allowed_diagnosis_scope, "allowed_diagnosis_scope"),
            (self.targeted_regression_requirements, "targeted_regression_requirements"),
            (self.escalation_conditions, "escalation_conditions"),
        ):
            _non_empty_tuple(value, name)
        if self.delivered_to_owner != self.responsible_root_cause_owner:
            raise NodeValidationError("FAILURE_FEEDBACK_OWNER_MISMATCH", "feedback must route to the responsible owner only")
        if self.broadcast:
            raise NodeValidationError("BROAD_FAILURE_FEEDBACK_PROHIBITED", "feedback cannot be broadcast")

    def as_dict(self) -> dict[str, Any]:
        return {
            "validation_receipt_identity": self.validation_receipt_identity,
            "failed_node_identity": self.failed_node_identity,
            "failed_criterion": self.failed_criterion,
            "reproduction_evidence_refs": list(self.reproduction_evidence_refs),
            "responsible_root_cause_owner": self.responsible_root_cause_owner,
            "repair_and_invalidation_graph_ref": self.repair_and_invalidation_graph_ref,
            "allowed_diagnosis_scope": list(self.allowed_diagnosis_scope),
            "frozen_state_ref": self.frozen_state_ref,
            "affected_descendant_refs": list(self.affected_descendant_refs),
            "targeted_regression_requirements": list(self.targeted_regression_requirements),
            "escalation_conditions": list(self.escalation_conditions),
            "delivered_to_owner": self.delivered_to_owner,
            "broadcast": False,
        }

    @property
    def package_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class RootCauseEvidence:
    reproduced_failure_ref: str
    localized_boundary_ref: str
    working_failing_comparison_ref: str
    hypothesis_ref: str
    hypothesis_test_result_ref: str
    selected_cause: str
    confidence_basis: str

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            _required_text(value, name)

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class RepairEligibilityReceipt:
    feedback_package_identity: str
    root_cause_evidence: RootCauseEvidence | None
    repair_eligible: bool
    block_reason: str

    @property
    def receipt_identity(self) -> str:
        return sha256_of(
            {
                "feedback_package_identity": self.feedback_package_identity,
                "root_cause_evidence": None if self.root_cause_evidence is None else self.root_cause_evidence.as_dict(),
                "repair_eligible": self.repair_eligible,
                "block_reason": self.block_reason,
            }
        )


def determine_repair_eligibility(
    feedback: FailureFeedbackPackage,
    root_cause: RootCauseEvidence | None,
) -> RepairEligibilityReceipt:
    if root_cause is None:
        return RepairEligibilityReceipt(feedback.package_identity, None, False, "ROOT_CAUSE_EVIDENCE_REQUIRED")
    return RepairEligibilityReceipt(feedback.package_identity, root_cause, True, "")


@dataclass(frozen=True)
class BoundedControlFlowPolicy:
    policy_id: str
    maximum_attempts: int
    timeout_seconds: int
    retryable_failure_classes: tuple[str, ...]
    non_retryable_failure_classes: tuple[str, ...]
    circuit_breaker_condition: str
    terminal_states: tuple[str, ...]
    escalation_destination: str
    loop_limit: int
    fan_out_limit: int
    arbitration_limit: int
    fallback_limit: int

    def __post_init__(self) -> None:
        _required_text(self.policy_id, "policy_id")
        for name in ("maximum_attempts", "timeout_seconds", "loop_limit", "fan_out_limit", "arbitration_limit", "fallback_limit"):
            if getattr(self, name) <= 0:
                raise NodeValidationError("UNBOUNDED_CONTROL_FLOW", f"{name} must be finite and positive")
        for value, name in (
            (self.retryable_failure_classes, "retryable_failure_classes"),
            (self.non_retryable_failure_classes, "non_retryable_failure_classes"),
            (self.terminal_states, "terminal_states"),
        ):
            _non_empty_tuple(value, name)
        _required_text(self.circuit_breaker_condition, "circuit_breaker_condition")
        _required_text(self.escalation_destination, "escalation_destination")

    @property
    def policy_identity(self) -> str:
        return sha256_of(self.__dict__)


@dataclass(frozen=True)
class ControlFlowValidationReceipt:
    policy_identity: str
    attempt_count: int
    circuit_open: bool
    terminal_state: str
    output_release_allowed: bool
    further_attempts_allowed: bool

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self.__dict__)


def validate_control_flow_state(
    policy: BoundedControlFlowPolicy,
    *,
    attempt_count: int,
    circuit_open: bool = False,
) -> ControlFlowValidationReceipt:
    if attempt_count < 0:
        raise NodeValidationError("INVALID_ATTEMPT_COUNT", "attempt count cannot be negative")
    exhausted = attempt_count >= policy.maximum_attempts
    terminal = "CIRCUIT_OPEN" if circuit_open else ("ATTEMPTS_EXHAUSTED" if exhausted else "READY")
    return ControlFlowValidationReceipt(
        policy_identity=policy.policy_identity,
        attempt_count=attempt_count,
        circuit_open=circuit_open,
        terminal_state=terminal,
        output_release_allowed=not circuit_open and not exhausted,
        further_attempts_allowed=not circuit_open and not exhausted,
    )


@dataclass(frozen=True)
class NodeValidationTransitionReceipt:
    action: NodeValidationAction
    prior_receipt_identity: str
    active_after: bool
    historical_receipt_preserved: bool
    command_identity: str
    authority_identity: str

    @property
    def transition_identity(self) -> str:
        return sha256_of(
            {
                "action": self.action.value,
                "prior_receipt_identity": self.prior_receipt_identity,
                "active_after": self.active_after,
                "historical_receipt_preserved": self.historical_receipt_preserved,
                "command_identity": self.command_identity,
                "authority_identity": self.authority_identity,
            }
        )


def compute_node_validation_transition_payload_sha256(
    receipt_identity: str,
    action: NodeValidationAction,
) -> str:
    return sha256_of({"receipt_identity": receipt_identity, "action": action.value})


def validate_repeat_node_validation(
    existing: NodeValidationReceipt,
    repeated: NodeValidationReceipt,
) -> NodeValidationReceipt:
    if existing.receipt_identity != repeated.receipt_identity:
        raise NodeValidationError("CONFLICTING_REPEAT_COMMAND", "validation payload differs")
    return existing


def invalidate_node_validation_receipt(
    receipt: NodeValidationReceipt,
    command: NodeValidationCommand,
    authority: NodeValidationAuthority,
) -> NodeValidationTransitionReceipt:
    return _transition(receipt, command, authority, NodeValidationAction.INVALIDATE)


def rollback_node_validation_receipt(
    receipt: NodeValidationReceipt,
    command: NodeValidationCommand,
    authority: NodeValidationAuthority,
) -> NodeValidationTransitionReceipt:
    return _transition(receipt, command, authority, NodeValidationAction.ROLLBACK)


def _transition(
    receipt: NodeValidationReceipt,
    command: NodeValidationCommand,
    authority: NodeValidationAuthority,
    action: NodeValidationAction,
) -> NodeValidationTransitionReceipt:
    receipt.as_dict()
    _check_command(
        command,
        authority,
        action,
        receipt.receipt_identity,
        compute_node_validation_transition_payload_sha256(receipt.receipt_identity, action),
    )
    return NodeValidationTransitionReceipt(
        action=action,
        prior_receipt_identity=receipt.receipt_identity,
        active_after=False,
        historical_receipt_preserved=True,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
    )


def _check_command(
    command: NodeValidationCommand,
    authority: NodeValidationAuthority,
    action: NodeValidationAction,
    resource_id: str,
    payload_sha256: str,
) -> None:
    if authority.status is not AuthorityStatus.ACTIVE:
        raise NodeValidationError("INACTIVE_AUTHORITY", "authority inactive")
    if action not in authority.permitted_actions or command.action is not action:
        raise NodeValidationError("UNAUTHORIZED_ACTION", "action not permitted")
    if resource_id not in authority.applicable_nodes and "*" not in authority.applicable_nodes:
        raise NodeValidationError("AUTHORITY_SCOPE_MISMATCH", "resource outside authority scope")
    if command.resource_id != resource_id:
        raise NodeValidationError("COMMAND_RESOURCE_MISMATCH", "resource mismatch")
    if command.payload_sha256 != payload_sha256:
        raise NodeValidationError("COMMAND_PAYLOAD_MISMATCH", "payload mismatch")
    if command.expected_authority_identity != authority.authority_identity:
        raise NodeValidationError("AUTHORITY_IDENTITY_MISMATCH", "authority mismatch")
