"""
Workflow Primitive Constitution & Checked Transfer Runtime Engine.

Governed by:
- Mandate CAE-M57 (Phase 07 - Workflow Engineering)
- Object Constitution CA-CAN-04 (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow; Agents own bounded reasoning within steps;
- Skills remain passive; Hooks provide deterministic event guarantees;
- State transitions follow checked transfer semantics (validate edge -> pre-checks -> out-hooks -> commit -> in-hooks);
- Failed blocking checks preserve the source state.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .pi_adapter import AuthorityLane


# ============================================================================
# 1. Error Taxonomy
# ============================================================================


class WorkflowPrimitiveError(RuntimeError):
    """Base class for all workflow primitive and control-flow errors."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "WORKFLOW_PRIMITIVE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class InvalidPrimitiveKindError(WorkflowPrimitiveError):
    """Raised when an unratified or invalid primitive kind is specified."""

    def __init__(self, kind: str) -> None:
        super().__init__(
            f"Unsupported or unratified workflow primitive kind: '{kind}'",
            reason_code="ERR_INVALID_PRIMITIVE_KIND",
            details={"kind": kind},
        )


class UnboundedLoopError(WorkflowPrimitiveError):
    """Raised when a LOOP primitive lacks a valid positive max_iterations bound."""

    def __init__(self, primitive_id: str, max_iterations: int) -> None:
        super().__init__(
            f"LOOP primitive '{primitive_id}' has invalid max_iterations={max_iterations}; must be > 0",
            reason_code="ERR_UNBOUNDED_LOOP",
            details={"primitive_id": primitive_id, "max_iterations": max_iterations},
        )


class AgentMutatedLoopBoundError(WorkflowPrimitiveError):
    """Raised when an agent attempts to mutate or override host-enforced loop bounds."""

    def __init__(self, primitive_id: str, attempted_by: str) -> None:
        super().__init__(
            f"Agent '{attempted_by}' attempted to mutate host loop bound for '{primitive_id}'; prohibited by INV-WFP-002",
            reason_code="ERR_AGENT_MUTATED_LOOP_BOUND",
            details={"primitive_id": primitive_id, "attempted_by": attempted_by},
        )


class UnevaluableConditionError(WorkflowPrimitiveError):
    """Raised when a condition predicate cannot be deterministically evaluated by host runtime."""

    def __init__(self, primitive_id: str, expression: str, reason: str) -> None:
        super().__init__(
            f"CONDITION primitive '{primitive_id}' cannot evaluate expression '{expression}': {reason}",
            reason_code="ERR_UNEVALUABLE_CONDITION",
            details={"primitive_id": primitive_id, "expression": expression, "reason": reason},
        )


class ParallelSideEffectConflictError(WorkflowPrimitiveError):
    """Raised when parallel branches contain conflicting non-read-only side-effect declarations."""

    def __init__(self, conflicting_branches: Sequence[str], side_effects: Sequence[str]) -> None:
        super().__init__(
            f"Parallel branches {conflicting_branches} contain conflicting mutating side effects {side_effects}; prohibited by INV-WFP-004",
            reason_code="ERR_PARALLEL_SIDE_EFFECT_CONFLICT",
            details={"conflicting_branches": list(conflicting_branches), "side_effects": list(side_effects)},
        )


class InvalidTransitionEdgeError(WorkflowPrimitiveError):
    """Raised when an attempted state transition is not declared in the state machine definition."""

    def __init__(self, from_state: str, to_state: str) -> None:
        super().__init__(
            f"Transition from '{from_state}' to '{to_state}' is not a valid declared edge",
            reason_code="ERR_INVALID_TRANSITION_EDGE",
            details={"from_state": from_state, "to_state": to_state},
        )


class BlockingPreTransferCheckFailedError(WorkflowPrimitiveError):
    """Raised when a blocking pre-transfer check fails, keeping execution in source state."""

    def __init__(self, check_name: str, source_state: str, target_state: str, failure_reason: str) -> None:
        super().__init__(
            f"Blocking pre-transfer check '{check_name}' failed for transfer '{source_state}' -> '{target_state}': {failure_reason}. Retained in '{source_state}'.",
            reason_code="ERR_BLOCKING_PRE_TRANSFER_CHECK_FAILED",
            details={
                "check_name": check_name,
                "source_state": source_state,
                "target_state": target_state,
                "failure_reason": failure_reason,
            },
        )


class StateRetentionViolationError(WorkflowPrimitiveError):
    """Raised when a runtime operation attempts to advance state despite a failed check."""

    def __init__(self, attempted_state: str, required_source_state: str) -> None:
        super().__init__(
            f"State retention violation: attempted to advance to '{attempted_state}' when failed check required retaining '{required_source_state}'",
            reason_code="ERR_STATE_RETENTION_VIOLATION",
            details={"attempted_state": attempted_state, "required_source_state": required_source_state},
        )


class UnsupportedPrimitiveError(WorkflowPrimitiveError):
    """Raised when an unsupported or improvised primitive is encountered."""

    def __init__(self, primitive_name: str) -> None:
        super().__init__(
            f"Workflow primitive '{primitive_name}' is unsupported by the ratified constitution",
            reason_code="ERR_UNSUPPORTED_PRIMITIVE",
            details={"primitive_name": primitive_name},
        )


class HumanGateBypassError(WorkflowPrimitiveError):
    """Raised when an attempt is made to bypass operator approval on a HUMAN_GATE."""

    def __init__(self, gate_id: str, attempted_by: str) -> None:
        super().__init__(
            f"Attempted to advance HUMAN_GATE '{gate_id}' by non-operator actor '{attempted_by}'; prohibited by INV-WFP-005",
            reason_code="ERR_HUMAN_GATE_BYPASS",
            details={"gate_id": gate_id, "attempted_by": attempted_by},
        )


# ============================================================================
# 2. Enums
# ============================================================================


class WorkflowPrimitiveKind(str, Enum):
    """The 14 ratified control-flow primitives in the Conscious Activation Engine."""

    SEQUENCE = "SEQUENCE"
    CONDITION = "CONDITION"
    SWITCH = "SWITCH"
    LOOP = "LOOP"
    RETRY = "RETRY"
    PARALLEL = "PARALLEL"
    JOIN = "JOIN"
    TIMEOUT = "TIMEOUT"
    WAIT = "WAIT"
    HUMAN_GATE = "HUMAN_GATE"
    FAIL = "FAIL"
    REPAIR = "REPAIR"
    CANCEL = "CANCEL"
    RESUME = "RESUME"


class WorkUnitKind(str, Enum):
    """The ratified execution work-unit kinds."""

    AGENT_CALL = "AGENT_CALL"
    CODE_FUNCTION = "CODE_FUNCTION"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class JoinPolicy(str, Enum):
    """Synchronization policies for JOIN primitives."""

    ALL = "ALL"
    ANY = "ANY"
    QUORUM = "QUORUM"


class LoopTerminationKind(str, Enum):
    """Host termination reasons for LOOP primitives."""

    MAX_ITERATIONS = "MAX_ITERATIONS"
    CONDITION_MET = "CONDITION_MET"
    EARLY_EXIT = "EARLY_EXIT"
    ERROR_ABORT = "ERROR_ABORT"


class RetryBackoffStrategy(str, Enum):
    """Backoff strategies for RETRY primitives."""

    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


# ============================================================================
# 3. Domain Dataclasses
# ============================================================================


@dataclass(frozen=True, slots=True)
class LoopBoundPolicy:
    """Host-enforced finite iteration policy for LOOP primitives."""

    max_iterations: int
    timeout_seconds: Optional[int] = None
    allow_agent_override: bool = False

    def __post_init__(self) -> None:
        if self.max_iterations <= 0:
            raise UnboundedLoopError("UNBOUNDED_LOOP", self.max_iterations)
        if self.allow_agent_override:
            raise AgentMutatedLoopBoundError("LOOP_CONFIG", "CONFIGURATION")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "max_iterations": self.max_iterations,
            "timeout_seconds": self.timeout_seconds,
            "allow_agent_override": False,
        }


@dataclass(frozen=True, slots=True)
class RetryPolicyDefinition:
    """Deterministic retry policy definition."""

    max_attempts: int
    backoff_strategy: RetryBackoffStrategy = RetryBackoffStrategy.CONSTANT
    initial_interval_seconds: int = 1
    max_interval_seconds: int = 60
    non_retryable_errors: Tuple[str, ...] = ()

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "max_attempts": self.max_attempts,
            "backoff_strategy": self.backoff_strategy.value,
            "initial_interval_seconds": self.initial_interval_seconds,
            "max_interval_seconds": self.max_interval_seconds,
            "non_retryable_errors": sorted(list(self.non_retryable_errors)),
        }


@dataclass(frozen=True, slots=True)
class ParallelBranchDefinition:
    """Definition of an individual concurrent branch in a PARALLEL primitive."""

    branch_id: str
    primitive_ref: str
    side_effect_class: str = "READ_ONLY"  # NONE, READ_ONLY, MUTATION_OPERATION

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "primitive_ref": self.primitive_ref,
            "side_effect_class": self.side_effect_class,
        }


@dataclass(frozen=True, slots=True)
class JoinCondition:
    """Synchronization criteria for a JOIN primitive."""

    policy: JoinPolicy = JoinPolicy.ALL
    quorum_count: Optional[int] = None
    timeout_seconds: Optional[int] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "policy": self.policy.value,
            "quorum_count": self.quorum_count,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass(frozen=True, slots=True)
class ConditionBranchDefinition:
    """Deterministic condition evaluation configuration."""

    condition_expression: str
    condition_fn_ref: Optional[str] = None
    then_step_id: str = ""
    else_step_id: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "condition_expression": self.condition_expression,
            "condition_fn_ref": self.condition_fn_ref,
            "then_step_id": self.then_step_id,
            "else_step_id": self.else_step_id,
        }


@dataclass(frozen=True, slots=True)
class SwitchCaseDefinition:
    """A discrete branch case for a SWITCH primitive."""

    match_value: str
    target_step_id: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "match_value": self.match_value,
            "target_step_id": self.target_step_id,
        }


@dataclass(frozen=True, slots=True)
class HumanGateRequirement:
    """Operator approval requirements for a HUMAN_GATE primitive."""

    gate_id: str
    required_lane: AuthorityLane = AuthorityLane.COMMANDER
    approver_role: str = "operator"
    timeout_seconds: Optional[int] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "required_lane": self.required_lane.value,
            "approver_role": self.approver_role,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass(frozen=True, slots=True)
class WorkflowStepContract:
    """Typed step contract for work units (AGENT_CALL, CODE_FUNCTION)."""

    step_id: str
    work_unit_kind: WorkUnitKind
    target_ref: str  # agent_id or function name
    input_schema_ref: str = ""
    output_schema_ref: str = ""
    authority_lane: AuthorityLane = AuthorityLane.ANALYST

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "work_unit_kind": self.work_unit_kind.value,
            "target_ref": self.target_ref,
            "input_schema_ref": self.input_schema_ref,
            "output_schema_ref": self.output_schema_ref,
            "authority_lane": self.authority_lane.value,
        }


@dataclass(frozen=True, slots=True)
class WorkflowTransitionSemantics:
    """Specification of checked transfer obligations for a state transition."""

    from_state: str
    to_state: str
    pre_transfer_checks: Tuple[str, ...] = ()
    out_hooks: Tuple[str, ...] = ()
    edge_guards: Tuple[str, ...] = ()
    in_hooks: Tuple[str, ...] = ()
    preserves_source_state_on_failure: bool = True

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "pre_transfer_checks": sorted(list(self.pre_transfer_checks)),
            "out_hooks": sorted(list(self.out_hooks)),
            "edge_guards": sorted(list(self.edge_guards)),
            "in_hooks": sorted(list(self.in_hooks)),
            "preserves_source_state_on_failure": self.preserves_source_state_on_failure,
        }


@dataclass(frozen=True, slots=True)
class CheckedTransferResult:
    """Outcome of a checked state transition execution."""

    success: bool
    from_state: str
    to_state: str
    current_state: str
    version_incremented: bool
    failed_check: Optional[str] = None
    failure_reason: Optional[str] = None
    executed_hooks: Tuple[str, ...] = ()
    context_refreshed: bool = False
    receipt_sha256: str = ""

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "current_state": self.current_state,
            "version_incremented": self.version_incremented,
            "failed_check": self.failed_check,
            "failure_reason": self.failure_reason,
            "executed_hooks": list(self.executed_hooks),
            "context_refreshed": self.context_refreshed,
            "receipt_sha256": self.receipt_sha256,
        }


@dataclass(frozen=True, slots=True)
class WorkflowPrimitiveDefinition:
    """Declarative, hash-addressed definition of a workflow primitive."""

    primitive_id: str
    primitive_kind: WorkflowPrimitiveKind
    work_unit_kind: WorkUnitKind = WorkUnitKind.NOT_APPLICABLE
    version: str = "1.0.0"
    step_contract: Optional[WorkflowStepContract] = None
    loop_policy: Optional[LoopBoundPolicy] = None
    retry_policy: Optional[RetryPolicyDefinition] = None
    condition_config: Optional[ConditionBranchDefinition] = None
    switch_cases: Tuple[SwitchCaseDefinition, ...] = ()
    default_switch_step: Optional[str] = None
    parallel_branches: Tuple[ParallelBranchDefinition, ...] = ()
    join_condition: Optional[JoinCondition] = None
    human_gate: Optional[HumanGateRequirement] = None
    timeout_seconds: Optional[int] = None
    transition_semantics: Optional[WorkflowTransitionSemantics] = None
    primitive_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not isinstance(self.primitive_kind, WorkflowPrimitiveKind):
            try:
                kind = WorkflowPrimitiveKind(self.primitive_kind)
                object.__setattr__(self, "primitive_kind", kind)
            except Exception:
                raise InvalidPrimitiveKindError(str(self.primitive_kind))

        if not isinstance(self.work_unit_kind, WorkUnitKind):
            try:
                wu_kind = WorkUnitKind(self.work_unit_kind)
                object.__setattr__(self, "work_unit_kind", wu_kind)
            except Exception:
                raise InvalidPrimitiveKindError(str(self.work_unit_kind))

        if not self.primitive_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "primitive_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "primitive_id": self.primitive_id,
            "primitive_kind": self.primitive_kind.value,
            "work_unit_kind": self.work_unit_kind.value,
            "version": self.version,
            "step_contract": self.step_contract.canonical_dict() if self.step_contract else None,
            "loop_policy": self.loop_policy.canonical_dict() if self.loop_policy else None,
            "retry_policy": self.retry_policy.canonical_dict() if self.retry_policy else None,
            "condition_config": self.condition_config.canonical_dict() if self.condition_config else None,
            "switch_cases": [sc.canonical_dict() for sc in self.switch_cases],
            "default_switch_step": self.default_switch_step,
            "parallel_branches": [pb.canonical_dict() for pb in self.parallel_branches],
            "join_condition": self.join_condition.canonical_dict() if self.join_condition else None,
            "human_gate": self.human_gate.canonical_dict() if self.human_gate else None,
            "timeout_seconds": self.timeout_seconds,
            "transition_semantics": self.transition_semantics.canonical_dict() if self.transition_semantics else None,
        }
        return data

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["primitive_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        return self._compute_sha256() == self.primitive_sha256


# ============================================================================
# 4. Workflow Primitive Validator & Checked Transfer Engine
# ============================================================================


class WorkflowPrimitiveValidator:
    """Structural and semantic validator enforcing constitutional laws and StateM alignment."""

    @classmethod
    def validate_primitive(cls, primitive: WorkflowPrimitiveDefinition) -> None:
        """Validate a primitive definition against all constitutional rules."""
        if not isinstance(primitive.primitive_kind, WorkflowPrimitiveKind):
            raise InvalidPrimitiveKindError(str(primitive.primitive_kind))

        # Check hash integrity
        if not primitive.verify_integrity():
            raise WorkflowPrimitiveError(
                f"Primitive '{primitive.primitive_id}' content hash mismatch",
                reason_code="ERR_PRIMITIVE_HASH_MISMATCH",
            )

        # Kind-specific validations
        if primitive.primitive_kind == WorkflowPrimitiveKind.LOOP:
            cls.validate_loop_bound(primitive.loop_policy)
        elif primitive.primitive_kind == WorkflowPrimitiveKind.CONDITION:
            cls.validate_condition(primitive.condition_config)
        elif primitive.primitive_kind == WorkflowPrimitiveKind.PARALLEL:
            cls.validate_parallel_branches(primitive.parallel_branches)
        elif primitive.primitive_kind == WorkflowPrimitiveKind.HUMAN_GATE:
            if not primitive.human_gate:
                raise WorkflowPrimitiveError(
                    f"HUMAN_GATE primitive '{primitive.primitive_id}' missing human_gate configuration",
                    reason_code="ERR_MISSING_HUMAN_GATE_CONFIG",
                )
        elif primitive.primitive_kind == WorkflowPrimitiveKind.SWITCH:
            if not primitive.switch_cases:
                raise WorkflowPrimitiveError(
                    f"SWITCH primitive '{primitive.primitive_id}' has empty switch_cases",
                    reason_code="ERR_EMPTY_SWITCH_CASES",
                )

        # Transition semantics check
        if primitive.transition_semantics:
            cls.validate_transition_semantics(primitive.transition_semantics)

    @classmethod
    def validate_loop_bound(cls, loop_policy: Optional[LoopBoundPolicy]) -> None:
        """Enforce INV-WFP-002: Bounded Iteration Law."""
        if loop_policy is None:
            raise UnboundedLoopError("MISSING_POLICY", 0)
        if loop_policy.max_iterations <= 0:
            raise UnboundedLoopError("INVALID_BOUND", loop_policy.max_iterations)
        if loop_policy.allow_agent_override:
            raise AgentMutatedLoopBoundError("LOOP_POLICY", "AGENT")

    @classmethod
    def validate_parallel_branches(cls, branches: Sequence[ParallelBranchDefinition]) -> None:
        """Enforce INV-WFP-004: Side-Effect Isolation Law in Parallelism."""
        if not branches:
            raise WorkflowPrimitiveError("PARALLEL primitive contains zero branches", reason_code="ERR_EMPTY_PARALLEL")

        mutating_branches: List[str] = []
        for b in branches:
            if b.side_effect_class not in {"NONE", "READ_ONLY"}:
                mutating_branches.append(b.branch_id)

        if len(mutating_branches) > 1:
            raise ParallelSideEffectConflictError(
                conflicting_branches=mutating_branches,
                side_effects=[b.side_effect_class for b in branches if b.branch_id in mutating_branches],
            )

    @classmethod
    def validate_condition(cls, condition: Optional[ConditionBranchDefinition]) -> None:
        """Validate condition expression and branch targets."""
        if condition is None:
            raise UnevaluableConditionError("MISSING_CONFIG", "", "ConditionBranchDefinition is required")
        if not condition.condition_expression.strip() and not condition.condition_fn_ref:
            raise UnevaluableConditionError(
                "EMPTY_EXPRESSION", condition.condition_expression, "Condition expression or function ref must be non-empty"
            )
        if not condition.then_step_id:
            raise UnevaluableConditionError("MISSING_THEN_STEP", condition.condition_expression, "then_step_id must be specified")

    @classmethod
    def validate_transition_semantics(
        cls,
        transition: WorkflowTransitionSemantics,
        allowed_edges: Optional[Sequence[Tuple[str, str]]] = None,
    ) -> None:
        """Enforce INV-WFP-003: Checked Transfer Law."""
        if not transition.from_state or not transition.to_state:
            raise InvalidTransitionEdgeError(transition.from_state, transition.to_state)

        if allowed_edges is not None:
            if (transition.from_state, transition.to_state) not in allowed_edges:
                raise InvalidTransitionEdgeError(transition.from_state, transition.to_state)

        if not transition.preserves_source_state_on_failure:
            raise StateRetentionViolationError(
                attempted_state=transition.to_state,
                required_source_state=transition.from_state,
            )

    @classmethod
    def execute_checked_transfer(
        cls,
        *,
        source_state: str,
        target_state: str,
        allowed_edges: Sequence[Tuple[str, str]],
        pre_transfer_predicates: Mapping[str, Callable[[], Tuple[bool, str]]],
        out_hooks: Sequence[Callable[[], None]] = (),
        edge_guards: Sequence[Callable[[], Tuple[bool, str]]] = (),
        in_hooks: Sequence[Callable[[], None]] = (),
        current_version: int = 1,
    ) -> CheckedTransferResult:
        """
        Execute the 6-stage checked transfer protocol per StateM Alignment Contract.

        Stages:
        1. Validate transition edge exists.
        2. Execute blocking pre-transfer checks. If any fails, retain source state.
        3. Execute persistence & out-hooks.
        4. Evaluate edge guards. If any fails, retain source state.
        5. Commit target state (increment version).
        6. Execute in-hooks and refresh entry context.
        """
        executed_hooks: List[str] = []

        # Stage 1: Edge validation
        if (source_state, target_state) not in allowed_edges:
            raise InvalidTransitionEdgeError(source_state, target_state)

        # Stage 2: Blocking Pre-Transfer Checks
        for check_name, check_fn in pre_transfer_predicates.items():
            passed, failure_reason = check_fn()
            if not passed:
                # Retain source state
                return CheckedTransferResult(
                    success=False,
                    from_state=source_state,
                    to_state=target_state,
                    current_state=source_state,  # Source state preserved!
                    version_incremented=False,
                    failed_check=check_name,
                    failure_reason=failure_reason,
                    executed_hooks=tuple(executed_hooks),
                    context_refreshed=False,
                    receipt_sha256="",
                )

        # Stage 3: Out-Hooks & Persistence
        for idx, out_hook in enumerate(out_hooks):
            hook_name = getattr(out_hook, "__name__", f"out_hook_{idx}")
            out_hook()
            executed_hooks.append(f"OUT:{hook_name}")

        # Stage 4: Edge Guards
        for idx, guard_fn in enumerate(edge_guards):
            guard_name = getattr(guard_fn, "__name__", f"guard_{idx}")
            passed, guard_reason = guard_fn()
            if not passed:
                return CheckedTransferResult(
                    success=False,
                    from_state=source_state,
                    to_state=target_state,
                    current_state=source_state,  # Source state preserved!
                    version_incremented=False,
                    failed_check=guard_name,
                    failure_reason=guard_reason,
                    executed_hooks=tuple(executed_hooks),
                    context_refreshed=False,
                    receipt_sha256="",
                )

        # Stage 5: Target State Commit
        committed_version = current_version + 1

        # Stage 6: In-Hooks & Entry Context Refresh
        for idx, in_hook in enumerate(in_hooks):
            hook_name = getattr(in_hook, "__name__", f"in_hook_{idx}")
            in_hook()
            executed_hooks.append(f"IN:{hook_name}")

        receipt_payload = {
            "from_state": source_state,
            "to_state": target_state,
            "committed_version": committed_version,
            "executed_hooks": executed_hooks,
        }
        receipt_sha256 = hashlib.sha256(canonical_json_text(receipt_payload).encode("utf-8")).hexdigest()

        return CheckedTransferResult(
            success=True,
            from_state=source_state,
            to_state=target_state,
            current_state=target_state,
            version_incremented=True,
            failed_check=None,
            failure_reason=None,
            executed_hooks=tuple(executed_hooks),
            context_refreshed=True,
            receipt_sha256=receipt_sha256,
        )
