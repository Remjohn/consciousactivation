"""Queue observability and local recovery proof contracts for ST-09.06."""

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


class ObservabilityRecoveryError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class QueueState(str, Enum):
    QUEUED = "queued"
    ELIGIBLE = "eligible"
    RUNNING = "running"
    WAITING_HUMAN = "waiting_human"
    BLOCKED = "blocked"
    RETRYING = "retrying"
    CANCELLED = "cancelled"
    PASSED = "passed"
    FAILED = "failed"
    SUPERSEDED = "superseded"


class FaultClass(str, Enum):
    AGENT_ERROR = "agent_error"
    MALFORMED_CONTRACT = "malformed_contract"
    DETERMINISTIC_CODE_FAILURE = "deterministic_code_failure"
    TIMEOUT = "timeout"
    LOST_OR_OUT_OF_ORDER_EVENT = "lost_or_out_of_order_event"
    SANDBOX_TERMINATION = "sandbox_termination"
    STALE_CHECKPOINT = "stale_checkpoint"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    PARTIAL_PARALLEL_FAILURE = "partial_parallel_failure"


class RecoveryAction(str, Enum):
    PROJECT = "PROJECT"
    RECOVER = "RECOVER"
    INVALIDATE = "INVALIDATE"
    ROLLBACK = "ROLLBACK"


class AuthorityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ObservabilityRecoveryError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _tuple(value: tuple[Any, ...], name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ObservabilityRecoveryError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class RecoveryAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[RecoveryAction, ...]
    applicable_scope: tuple[str, ...]
    status: AuthorityStatus = AuthorityStatus.ACTIVE

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
class RecoveryCommand:
    command_id: str
    action: RecoveryAction
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
class QueueEvent:
    event_id: str
    sequence: int
    workflow_identity: str
    node_identity: str
    state: QueueState
    reason: str
    causal_event_refs: tuple[str, ...]
    actor_identity: str
    authority_ref: str
    checkpoint_ref: str
    artifact_refs: tuple[str, ...]
    invalidated: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.event_id, "event_id"),
            (self.workflow_identity, "workflow_identity"),
            (self.node_identity, "node_identity"),
            (self.reason, "reason"),
            (self.actor_identity, "actor_identity"),
            (self.authority_ref, "authority_ref"),
            (self.checkpoint_ref, "checkpoint_ref"),
        ):
            _text(value, name)
        if self.sequence < 0:
            raise ObservabilityRecoveryError("INVALID_EVENT_SEQUENCE", "sequence cannot be negative")

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "sequence": self.sequence,
            "workflow_identity": self.workflow_identity,
            "node_identity": self.node_identity,
            "state": self.state.value,
            "reason": self.reason,
            "causal_event_refs": list(self.causal_event_refs),
            "actor_identity": self.actor_identity,
            "authority_ref": self.authority_ref,
            "checkpoint_ref": self.checkpoint_ref,
            "artifact_refs": list(self.artifact_refs),
            "invalidated": self.invalidated,
        }


@dataclass(frozen=True)
class QueueProjection:
    workflow_identity: str
    node_states: dict[str, str]
    transition_reasons: dict[str, str]
    event_identities: tuple[str, ...]
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "workflow_identity": self.workflow_identity,
            "node_states": self.node_states,
            "transition_reasons": self.transition_reasons,
            "event_identities": list(self.event_identities),
        }

    @property
    def projection_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        identity = sha256_of(payload)
        if identity != self._anchor:
            raise ObservabilityRecoveryError("MUTATED_GOVERNED_OBJECT", "projection changed")
        payload["projection_identity"] = identity
        return payload


def project_queue(events: tuple[QueueEvent, ...]) -> QueueProjection:
    _tuple(events, "events")
    ordered = sorted(events, key=lambda event: event.sequence)
    if [event.sequence for event in ordered] != list(range(len(ordered))):
        raise ObservabilityRecoveryError("OUT_OF_ORDER_EVENT_STREAM", "event stream must be contiguous")
    if len({event.event_id for event in ordered}) != len(ordered):
        raise ObservabilityRecoveryError("DUPLICATE_EVENT", "event ids must be unique")
    workflow_ids = {event.workflow_identity for event in ordered}
    if len(workflow_ids) != 1:
        raise ObservabilityRecoveryError("CONFLICTING_WORKFLOW_EVENTS", "one workflow per projection")
    node_states: dict[str, str] = {}
    reasons: dict[str, str] = {}
    for event in ordered:
        if event.invalidated:
            continue
        node_states[event.node_identity] = event.state.value
        reasons[event.node_identity] = event.reason
    return QueueProjection(next(iter(workflow_ids)), node_states, reasons, tuple(sha256_of(event.as_dict()) for event in ordered))


@dataclass(frozen=True)
class NodeTelemetry:
    node_identity: str
    actor_identity: str
    contract_version: str
    start_observation_ref: str
    end_observation_ref: str
    queue_wait_ms: int
    execution_latency_ms: int
    deterministic_compute_units: int
    model_token_observation: str
    cost_observation: str
    tool_calls: tuple[str, ...]
    capability_grants: tuple[str, ...]
    attempts: int
    retries: int
    circuit_state: str
    cache_behavior: str
    sandbox_policy_ref: str
    artifact_refs: tuple[str, ...]
    validation_refs: tuple[str, ...]
    human_interventions: tuple[str, ...]
    final_status: str
    failure_context: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.node_identity, "node_identity"),
            (self.actor_identity, "actor_identity"),
            (self.contract_version, "contract_version"),
            (self.start_observation_ref, "start_observation_ref"),
            (self.end_observation_ref, "end_observation_ref"),
            (self.model_token_observation, "model_token_observation"),
            (self.cost_observation, "cost_observation"),
            (self.circuit_state, "circuit_state"),
            (self.cache_behavior, "cache_behavior"),
            (self.sandbox_policy_ref, "sandbox_policy_ref"),
            (self.final_status, "final_status"),
        ):
            _text(value, name)
        if min(self.queue_wait_ms, self.execution_latency_ms, self.deterministic_compute_units, self.attempts, self.retries) < 0:
            raise ObservabilityRecoveryError("NEGATIVE_TELEMETRY_VALUE", "telemetry values cannot be negative")
        _tuple(self.artifact_refs, "artifact_refs")
        _tuple(self.validation_refs, "validation_refs")

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "tool_calls": list(self.tool_calls),
            "capability_grants": list(self.capability_grants),
            "artifact_refs": list(self.artifact_refs),
            "validation_refs": list(self.validation_refs),
            "human_interventions": list(self.human_interventions),
        }

    @property
    def telemetry_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class BudgetLimits:
    expected_tokens: int
    hard_token_limit: int
    expected_latency_ms: int
    hard_latency_limit_ms: int
    expected_cost_units: int
    hard_cost_limit_units: int
    deterministic_compute_limit: int
    overflow_policy_ref: str

    def __post_init__(self) -> None:
        _text(self.overflow_policy_ref, "overflow_policy_ref")
        if self.hard_token_limit <= 0 or self.hard_latency_limit_ms <= 0 or self.hard_cost_limit_units <= 0 or self.deterministic_compute_limit <= 0:
            raise ObservabilityRecoveryError("UNBOUNDED_BUDGET", "hard limits are required")


@dataclass(frozen=True)
class BudgetValidationReceipt:
    telemetry_identity: str
    budget_identity: str
    within_budget: bool
    blocked_reason: str
    human_gate_ref: str

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self.__dict__)


def validate_budget(telemetry: NodeTelemetry, limits: BudgetLimits, *, observed_tokens: int, observed_cost_units: int) -> BudgetValidationReceipt:
    over = []
    if observed_tokens > limits.hard_token_limit:
        over.append("hard_token_limit")
    if telemetry.execution_latency_ms > limits.hard_latency_limit_ms:
        over.append("hard_latency_limit")
    if observed_cost_units > limits.hard_cost_limit_units:
        over.append("hard_cost_limit")
    if telemetry.deterministic_compute_units > limits.deterministic_compute_limit:
        over.append("deterministic_compute_limit")
    return BudgetValidationReceipt(
        telemetry.telemetry_identity,
        sha256_of(limits.__dict__),
        not over,
        ",".join(over),
        "" if not over else limits.overflow_policy_ref,
    )


@dataclass(frozen=True)
class PublicSeamReceipt:
    projection_identity: str
    telemetry_identities: tuple[str, ...]
    budget_receipts: tuple[str, ...]
    route_refs: tuple[str, ...]
    checkpoint_refs: tuple[str, ...]
    public_contract_only: bool = True
    private_state_used: bool = False

    def __post_init__(self) -> None:
        if self.private_state_used:
            raise ObservabilityRecoveryError("PRIVATE_STATE_AS_PUBLIC_SEAM_EVIDENCE", "public seam cannot use private state")
        _tuple(self.telemetry_identities, "telemetry_identities")

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self.__dict__)


@dataclass(frozen=True)
class FaultFixture:
    fixture_id: str
    fault_class: FaultClass
    injected_observation_ref: str
    affected_node: str
    expected_state: QueueState
    repair_or_escalation_route: str
    external_fault_executed: bool = False

    def __post_init__(self) -> None:
        if self.external_fault_executed:
            raise ObservabilityRecoveryError("EXTERNAL_FAULT_EXECUTION_PROHIBITED", "faults are injected observations only")
        for value, name in ((self.fixture_id, "fixture_id"), (self.injected_observation_ref, "injected_observation_ref"), (self.affected_node, "affected_node"), (self.repair_or_escalation_route, "repair_or_escalation_route")):
            _text(value, name)


@dataclass(frozen=True)
class RecoveryReceipt:
    fixture_identity: str
    contained_state: str
    repair_or_escalation_route: str
    unaffected_branches_preserved: tuple[str, ...]
    resume_eligible: bool
    rollback_eligible: bool
    partial_state_created: bool = False

    def __post_init__(self) -> None:
        if self.partial_state_created:
            raise ObservabilityRecoveryError("PARTIAL_RECOVERY_STATE_PROHIBITED", "fault recovery cannot create partial state")
        _tuple(self.unaffected_branches_preserved, "unaffected_branches_preserved")

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self.__dict__)


def inject_fault_and_recover(fixture: FaultFixture, unaffected_branches: tuple[str, ...]) -> RecoveryReceipt:
    return RecoveryReceipt(
        sha256_of(fixture.__dict__ | {"fault_class": fixture.fault_class.value, "expected_state": fixture.expected_state.value}),
        fixture.expected_state.value,
        fixture.repair_or_escalation_route,
        unaffected_branches,
        fixture.fault_class not in {FaultClass.MALFORMED_CONTRACT, FaultClass.PROVIDER_UNAVAILABLE},
        True,
        False,
    )


@dataclass(frozen=True)
class RecoveryTransitionReceipt:
    action: RecoveryAction
    prior_identity: str
    active_after: bool
    historical_receipt_preserved: bool
    command_identity: str
    authority_identity: str

    @property
    def transition_identity(self) -> str:
        return sha256_of(self.__dict__ | {"action": self.action.value})


def compute_transition_payload_sha256(prior_identity: str, action: RecoveryAction) -> str:
    return sha256_of({"prior_identity": prior_identity, "action": action.value})


def invalidate_projection(prior_identity: str, command: RecoveryCommand, authority: RecoveryAuthority) -> RecoveryTransitionReceipt:
    _check(command, authority, RecoveryAction.INVALIDATE, prior_identity, compute_transition_payload_sha256(prior_identity, RecoveryAction.INVALIDATE))
    return RecoveryTransitionReceipt(RecoveryAction.INVALIDATE, prior_identity, False, True, command.command_identity, authority.authority_identity)


def rollback_projection(prior_identity: str, command: RecoveryCommand, authority: RecoveryAuthority) -> RecoveryTransitionReceipt:
    _check(command, authority, RecoveryAction.ROLLBACK, prior_identity, compute_transition_payload_sha256(prior_identity, RecoveryAction.ROLLBACK))
    return RecoveryTransitionReceipt(RecoveryAction.ROLLBACK, prior_identity, False, True, command.command_identity, authority.authority_identity)


def validate_repeat_projection(existing_identity: str, repeated_identity: str) -> str:
    if existing_identity != repeated_identity:
        raise ObservabilityRecoveryError("CONFLICTING_REPEAT_COMMAND", "projection payload differs")
    return existing_identity


def _check(command: RecoveryCommand, authority: RecoveryAuthority, action: RecoveryAction, resource_id: str, payload_sha256: str) -> None:
    if authority.status is not AuthorityStatus.ACTIVE:
        raise ObservabilityRecoveryError("INACTIVE_AUTHORITY", "authority inactive")
    if action not in authority.permitted_actions or command.action is not action:
        raise ObservabilityRecoveryError("UNAUTHORIZED_ACTION", "action not permitted")
    if resource_id not in authority.applicable_scope and "*" not in authority.applicable_scope:
        raise ObservabilityRecoveryError("AUTHORITY_SCOPE_MISMATCH", "resource outside authority")
    if command.resource_id != resource_id:
        raise ObservabilityRecoveryError("COMMAND_RESOURCE_MISMATCH", "resource mismatch")
    if command.payload_sha256 != payload_sha256:
        raise ObservabilityRecoveryError("COMMAND_PAYLOAD_MISMATCH", "payload mismatch")
    if command.expected_authority_identity != authority.authority_identity:
        raise ObservabilityRecoveryError("AUTHORITY_IDENTITY_MISMATCH", "authority mismatch")
