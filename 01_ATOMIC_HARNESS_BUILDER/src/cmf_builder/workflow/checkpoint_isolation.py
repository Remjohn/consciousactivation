"""Local checkpoint, sandbox declaration and safe-resume contracts for ST-09.04."""

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


class CheckpointIsolationError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CheckpointAction(str, Enum):
    COMMIT = "COMMIT"
    RESUME = "RESUME"
    INVALIDATE = "INVALIDATE"
    ROLLBACK = "ROLLBACK"


class AuthorityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"


class SandboxClass(str, Enum):
    DETERMINISTIC_PROCESS = "deterministic_process_sandbox"
    PROVIDER_CALL = "provider_call_sandbox"
    ISOLATED_IMPLEMENTATION_TASK = "isolated_implementation_task_sandbox"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CheckpointIsolationError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _tuple(value: tuple[Any, ...], name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise CheckpointIsolationError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class CheckpointAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[CheckpointAction, ...]
    applicable_runs: tuple[str, ...]
    status: AuthorityStatus = AuthorityStatus.ACTIVE

    def __post_init__(self) -> None:
        _text(self.authority_id, "authority_id")
        _text(self.authority_version, "authority_version")
        _text(self.authority_sha256, "authority_sha256")
        _tuple(self.permitted_actions, "permitted_actions")
        _tuple(self.applicable_runs, "applicable_runs")

    @property
    def authority_identity(self) -> str:
        return sha256_of(
            {
                "authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_sha256": self.authority_sha256,
                "permitted_actions": [action.value for action in self.permitted_actions],
                "applicable_runs": list(self.applicable_runs),
                "status": self.status.value,
            }
        )


@dataclass(frozen=True)
class CheckpointCommand:
    command_id: str
    action: CheckpointAction
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
class SideEffectRecord:
    side_effect_id: str
    idempotency_key: str
    effect_hash: str
    committed: bool
    human_action: bool = False

    def __post_init__(self) -> None:
        _text(self.side_effect_id, "side_effect_id")
        _text(self.idempotency_key, "idempotency_key")
        _text(self.effect_hash, "effect_hash")

    def as_dict(self) -> dict[str, Any]:
        return {
            "side_effect_id": self.side_effect_id,
            "idempotency_key": self.idempotency_key,
            "effect_hash": self.effect_hash,
            "committed": self.committed,
            "human_action": self.human_action,
        }


@dataclass(frozen=True)
class WorkflowCheckpoint:
    checkpoint_id: str
    checkpoint_version: str
    run_id: str
    workflow_hash: str
    profile_hash: str
    completed_node_identities: tuple[str, ...]
    committed_input_hashes: tuple[str, ...]
    committed_output_hashes: tuple[str, ...]
    node_validation_receipt_refs: tuple[str, ...]
    side_effect_records: tuple[SideEffectRecord, ...]
    event_stream_position: int
    next_eligible_nodes: tuple[str, ...]
    parent_checkpoint_ref: str
    invalidation_refs: tuple[str, ...]
    authority_identity: str
    active: bool = True
    invalidated: bool = False
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for value, name in (
            (self.checkpoint_id, "checkpoint_id"),
            (self.checkpoint_version, "checkpoint_version"),
            (self.run_id, "run_id"),
            (self.workflow_hash, "workflow_hash"),
            (self.profile_hash, "profile_hash"),
            (self.authority_identity, "authority_identity"),
        ):
            _text(value, name)
        if self.event_stream_position < 0:
            raise CheckpointIsolationError("INVALID_EVENT_POSITION", "event stream position cannot be negative")
        if len({record.idempotency_key for record in self.side_effect_records}) != len(self.side_effect_records):
            raise CheckpointIsolationError("DUPLICATE_SIDE_EFFECT_IDEMPOTENCY_KEY", "side effects must be idempotent")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "checkpoint_version": self.checkpoint_version,
            "run_id": self.run_id,
            "workflow_hash": self.workflow_hash,
            "profile_hash": self.profile_hash,
            "completed_node_identities": list(self.completed_node_identities),
            "committed_input_hashes": list(self.committed_input_hashes),
            "committed_output_hashes": list(self.committed_output_hashes),
            "node_validation_receipt_refs": list(self.node_validation_receipt_refs),
            "side_effect_records": [record.as_dict() for record in self.side_effect_records],
            "event_stream_position": self.event_stream_position,
            "next_eligible_nodes": list(self.next_eligible_nodes),
            "parent_checkpoint_ref": self.parent_checkpoint_ref,
            "invalidation_refs": list(self.invalidation_refs),
            "authority_identity": self.authority_identity,
            "active": self.active,
            "invalidated": self.invalidated,
            "external_engine_reconstruction": "NOT_IMPLEMENTED_EXTERNAL_VALIDATION_PENDING",
            "production_ready": False,
            "certified": False,
        }

    @property
    def checkpoint_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        identity = sha256_of(payload)
        if identity != self._anchor:
            raise CheckpointIsolationError("MUTATED_GOVERNED_OBJECT", "checkpoint changed after commit")
        payload["checkpoint_identity"] = identity
        return payload


def compute_checkpoint_payload_sha256(**values: Any) -> str:
    normalized = dict(values)
    if "side_effect_records" in normalized:
        normalized["side_effect_records"] = [record.as_dict() for record in normalized["side_effect_records"]]
    return sha256_of(normalized)


def commit_checkpoint(command: CheckpointCommand, authority: CheckpointAuthority, **values: Any) -> WorkflowCheckpoint:
    run_id = str(values.get("run_id", ""))
    _check(command, authority, CheckpointAction.COMMIT, run_id, compute_checkpoint_payload_sha256(**values))
    return WorkflowCheckpoint(authority_identity=authority.authority_identity, **values)


@dataclass(frozen=True)
class ResumeRequest:
    run_id: str
    workflow_hash: str
    profile_hash: str
    node_id: str
    attempt_policy_hash: str
    input_hash: str

    @property
    def idempotency_key(self) -> str:
        return sha256_of(self.__dict__)


@dataclass(frozen=True)
class ResumeReceipt:
    checkpoint_identity: str
    request_idempotency_key: str
    reused_node_outputs: tuple[str, ...]
    next_eligible_nodes: tuple[str, ...]
    duplicate_side_effects_prevented: tuple[str, ...]
    ratified_human_actions_replayed: bool
    active_after: bool
    command_identity: str

    @property
    def receipt_identity(self) -> str:
        return sha256_of(
            {
                "checkpoint_identity": self.checkpoint_identity,
                "request_idempotency_key": self.request_idempotency_key,
                "reused_node_outputs": list(self.reused_node_outputs),
                "next_eligible_nodes": list(self.next_eligible_nodes),
                "duplicate_side_effects_prevented": list(self.duplicate_side_effects_prevented),
                "ratified_human_actions_replayed": self.ratified_human_actions_replayed,
                "active_after": self.active_after,
                "command_identity": self.command_identity,
            }
        )


def compute_resume_payload_sha256(checkpoint: WorkflowCheckpoint, request: ResumeRequest) -> str:
    return sha256_of({"checkpoint_identity": checkpoint.checkpoint_identity, "request": request.__dict__})


def resume_checkpoint(
    checkpoint: WorkflowCheckpoint,
    request: ResumeRequest,
    command: CheckpointCommand,
    authority: CheckpointAuthority,
) -> ResumeReceipt:
    if not checkpoint.active or checkpoint.invalidated:
        raise CheckpointIsolationError("STALE_OR_INVALIDATED_CHECKPOINT", "checkpoint cannot resume")
    _check(command, authority, CheckpointAction.RESUME, checkpoint.checkpoint_identity, compute_resume_payload_sha256(checkpoint, request))
    if request.run_id != checkpoint.run_id:
        raise CheckpointIsolationError("RUN_ID_MISMATCH", "resume run differs")
    if request.workflow_hash != checkpoint.workflow_hash:
        raise CheckpointIsolationError("WORKFLOW_HASH_MISMATCH", "workflow changed")
    if request.profile_hash != checkpoint.profile_hash:
        raise CheckpointIsolationError("SILENT_PROFILE_CHANGE_PROHIBITED", "profile changed")
    if request.node_id not in checkpoint.next_eligible_nodes:
        raise CheckpointIsolationError("NODE_NOT_ELIGIBLE_FOR_RESUME", "only eligible nodes can resume")
    duplicate_keys = tuple(record.idempotency_key for record in checkpoint.side_effect_records if record.committed)
    return ResumeReceipt(
        checkpoint.checkpoint_identity,
        request.idempotency_key,
        checkpoint.committed_output_hashes,
        checkpoint.next_eligible_nodes,
        duplicate_keys,
        False,
        True,
        command.command_identity,
    )


@dataclass(frozen=True)
class SandboxPolicyDeclaration:
    policy_id: str
    sandbox_class: SandboxClass
    immutable_environment_ref: str
    read_only_evidence_mounts: tuple[str, ...]
    writable_staging_paths: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    network_allowlist: tuple[str, ...]
    secret_reference_names: tuple[str, ...]
    cpu_limit: str
    memory_limit: str
    time_limit_seconds: int
    output_contract: str
    logging_redaction_policy: str
    disposal_policy: str
    isolation_mechanism_class: str
    deny_by_default: bool = True
    execution_performed: bool = False

    def __post_init__(self) -> None:
        if not self.deny_by_default:
            raise CheckpointIsolationError("SANDBOX_NOT_DENY_BY_DEFAULT", "sandbox must deny undeclared capability")
        if self.execution_performed:
            raise CheckpointIsolationError("SANDBOX_EXECUTION_PROHIBITED", "policy declaration cannot execute")
        for value, name in (
            (self.policy_id, "policy_id"),
            (self.immutable_environment_ref, "immutable_environment_ref"),
            (self.cpu_limit, "cpu_limit"),
            (self.memory_limit, "memory_limit"),
            (self.output_contract, "output_contract"),
            (self.logging_redaction_policy, "logging_redaction_policy"),
            (self.disposal_policy, "disposal_policy"),
            (self.isolation_mechanism_class, "isolation_mechanism_class"),
        ):
            _text(value, name)
        for value, name in (
            (self.read_only_evidence_mounts, "read_only_evidence_mounts"),
            (self.writable_staging_paths, "writable_staging_paths"),
        ):
            _tuple(value, name)
        if self.time_limit_seconds <= 0:
            raise CheckpointIsolationError("UNBOUNDED_SANDBOX_LIFETIME", "time limit required")
        for secret_ref in self.secret_reference_names:
            if "=" in secret_ref or secret_ref.lower().startswith(("sk-", "secret:", "token:")):
                raise CheckpointIsolationError("SECRET_VALUE_PROHIBITED", "only secret reference names are permitted")
        if self.sandbox_class is SandboxClass.PROVIDER_CALL and self.network_allowlist == ("*",):
            raise CheckpointIsolationError("UNDECLARED_NETWORK_ACCESS", "provider sandbox requires exact allowlist")

    def as_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "sandbox_class": self.sandbox_class.value,
            "immutable_environment_ref": self.immutable_environment_ref,
            "read_only_evidence_mounts": list(self.read_only_evidence_mounts),
            "writable_staging_paths": list(self.writable_staging_paths),
            "allowed_tools": list(self.allowed_tools),
            "network_allowlist": list(self.network_allowlist),
            "secret_reference_names": list(self.secret_reference_names),
            "cpu_limit": self.cpu_limit,
            "memory_limit": self.memory_limit,
            "time_limit_seconds": self.time_limit_seconds,
            "output_contract": self.output_contract,
            "logging_redaction_policy": self.logging_redaction_policy,
            "disposal_policy": self.disposal_policy,
            "isolation_mechanism_class": self.isolation_mechanism_class,
            "deny_by_default": True,
            "execution_performed": False,
        }

    @property
    def policy_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class ParallelWorkUnit:
    unit_id: str
    dependency_unit_ids: tuple[str, ...]
    write_set: tuple[str, ...]
    authority_ref: str

    def __post_init__(self) -> None:
        _text(self.unit_id, "unit_id")
        _text(self.authority_ref, "authority_ref")
        _tuple(self.write_set, "write_set")

    def as_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "dependency_unit_ids": list(self.dependency_unit_ids),
            "write_set": list(self.write_set),
            "authority_ref": self.authority_ref,
        }


@dataclass(frozen=True)
class ParallelPlan:
    plan_id: str
    units: tuple[ParallelWorkUnit, ...]
    concurrency_limit: int
    budget_limit: str
    cancellation_policy: str
    merge_policy: str
    conflict_policy: str
    terminal_states: tuple[str, ...]
    execution_performed: bool = False

    def __post_init__(self) -> None:
        _text(self.plan_id, "plan_id")
        if self.concurrency_limit <= 0:
            raise CheckpointIsolationError("UNBOUNDED_PARALLELISM", "concurrency limit required")
        for value, name in (
            (self.budget_limit, "budget_limit"),
            (self.cancellation_policy, "cancellation_policy"),
            (self.merge_policy, "merge_policy"),
            (self.conflict_policy, "conflict_policy"),
        ):
            _text(value, name)
        _tuple(self.units, "units")
        _tuple(self.terminal_states, "terminal_states")
        if self.execution_performed:
            raise CheckpointIsolationError("PARALLEL_EXECUTION_PROHIBITED", "plan is declaration only")
        by_id = {unit.unit_id: unit for unit in self.units}
        if len(by_id) != len(self.units):
            raise CheckpointIsolationError("DUPLICATE_PARALLEL_UNIT", "unit ids must be unique")
        for unit in self.units:
            if set(unit.dependency_unit_ids) & set(by_id):
                raise CheckpointIsolationError("DEPENDENCY_UNSAFE_PARALLELISM", "concurrent units cannot depend on each other")
        seen_writes: dict[str, str] = {}
        for unit in self.units:
            for path in unit.write_set:
                owner = seen_writes.setdefault(path, unit.unit_id)
                if owner != unit.unit_id:
                    raise CheckpointIsolationError("SHARED_WRITE_PARALLELISM", "write sets must be disjoint")

    def as_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "units": [unit.as_dict() for unit in self.units],
            "concurrency_limit": self.concurrency_limit,
            "budget_limit": self.budget_limit,
            "cancellation_policy": self.cancellation_policy,
            "merge_policy": self.merge_policy,
            "conflict_policy": self.conflict_policy,
            "terminal_states": list(self.terminal_states),
            "execution_performed": False,
        }

    @property
    def plan_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class CheckpointTransitionReceipt:
    action: CheckpointAction
    prior_checkpoint_identity: str
    active_after: bool
    historical_checkpoint_preserved: bool
    command_identity: str
    authority_identity: str

    @property
    def transition_identity(self) -> str:
        return sha256_of(
            {
                "action": self.action.value,
                "prior_checkpoint_identity": self.prior_checkpoint_identity,
                "active_after": self.active_after,
                "historical_checkpoint_preserved": self.historical_checkpoint_preserved,
                "command_identity": self.command_identity,
                "authority_identity": self.authority_identity,
            }
        )


def validate_repeat_checkpoint(existing: WorkflowCheckpoint, repeated: WorkflowCheckpoint) -> WorkflowCheckpoint:
    if existing.checkpoint_identity != repeated.checkpoint_identity:
        raise CheckpointIsolationError("CONFLICTING_REPEAT_COMMAND", "checkpoint payload differs")
    return existing


def compute_checkpoint_transition_payload_sha256(checkpoint_identity: str, action: CheckpointAction) -> str:
    return sha256_of({"checkpoint_identity": checkpoint_identity, "action": action.value})


def invalidate_checkpoint(
    checkpoint: WorkflowCheckpoint,
    command: CheckpointCommand,
    authority: CheckpointAuthority,
) -> CheckpointTransitionReceipt:
    return _transition(checkpoint, command, authority, CheckpointAction.INVALIDATE)


def rollback_checkpoint(
    checkpoint: WorkflowCheckpoint,
    command: CheckpointCommand,
    authority: CheckpointAuthority,
) -> CheckpointTransitionReceipt:
    return _transition(checkpoint, command, authority, CheckpointAction.ROLLBACK)


def _transition(
    checkpoint: WorkflowCheckpoint,
    command: CheckpointCommand,
    authority: CheckpointAuthority,
    action: CheckpointAction,
) -> CheckpointTransitionReceipt:
    checkpoint.as_dict()
    _check(command, authority, action, checkpoint.checkpoint_identity, compute_checkpoint_transition_payload_sha256(checkpoint.checkpoint_identity, action))
    return CheckpointTransitionReceipt(action, checkpoint.checkpoint_identity, False, True, command.command_identity, authority.authority_identity)


def _check(
    command: CheckpointCommand,
    authority: CheckpointAuthority,
    action: CheckpointAction,
    resource_id: str,
    payload_sha256: str,
) -> None:
    if authority.status is not AuthorityStatus.ACTIVE:
        raise CheckpointIsolationError("INACTIVE_AUTHORITY", "authority inactive")
    if action not in authority.permitted_actions or command.action is not action:
        raise CheckpointIsolationError("UNAUTHORIZED_ACTION", "action not permitted")
    if resource_id not in authority.applicable_runs and "*" not in authority.applicable_runs:
        raise CheckpointIsolationError("AUTHORITY_SCOPE_MISMATCH", "resource outside authority")
    if command.resource_id != resource_id:
        raise CheckpointIsolationError("COMMAND_RESOURCE_MISMATCH", "resource mismatch")
    if command.payload_sha256 != payload_sha256:
        raise CheckpointIsolationError("COMMAND_PAYLOAD_MISMATCH", "payload mismatch")
    if command.expected_authority_identity != authority.authority_identity:
        raise CheckpointIsolationError("AUTHORITY_IDENTITY_MISMATCH", "authority mismatch")
