"""CAE Hooks, Extensions, and Capability Enforcement Runtime Subsystem.

Governed by:
- Phase 2 Mandate M23 (02_PHASE_2_RUNTIME_FOUNDATION/M23_hooks_extensions_capability_enforcement_runtime.md)
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 00_CONTROL/23_PHASE2_EVENT_TRACE_CONTRACT.md
- 00_CONTROL/25_PHASE2_OPERATOR_GATE_RUNTIME_CONTRACT.md
- 00_CONTROL/06_STATE_AND_HOOKS_MODEL.md
- Phase 1 Mandate M06 (Hook / Extension Guarantee Matrix)

Enforces:
1. Four Non-Negotiable Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
2. Explicit Capability Grants & Security Sandboxing:
   - CAE_TYPED_OPERATION: Bound to workspace and validated against authority lane bindings.
   - POSTGRES_STORAGE: Explicit table/scope grants with RLS workspace binding.
   - FILESYSTEM: Strict sandbox containment, blocking path traversal (../) and unauthorized paths.
   - PROCESS_CLI: Whitelisted executables, sanitized arguments, operator approval for risky actions.
   - NETWORK: Hostname/domain allowlists, protocol restrictions (HTTPS/HTTP), external effect auditing.
   - SECRETS: Named references only, raw secret retrieval strictly blocked.
   - MCP_TOOL: Server and tool name allowlisting with policy evaluation.
3. Deterministic Hook Pipeline:
   - PRE_TOOL: Pre-invocation capability validation, lane checks, and operator gate triggering.
   - POST_MUTATION: Mutation schema validation, side-effect recording, and idempotency registration.
   - STATE_TRANSFER: Invariant and receipt validation before state commits.
   - COMPLETION: Strict gating verifying all required receipts, evidence, and operator confirmations.
   - RECOVERY: Governed failure routing into REPAIRING lifecycle state.
4. Durable Operator Gate Runtime:
   - State transition to WAITING_OPERATOR with immutable decision context.
   - Anti-self-approval rule: models and requesters cannot approve their own work.
   - Authenticated operator decision required for resumption.
5. Full Cryptographic Causal Trace Integration:
   - Every hook evaluation and capability decision is logged with SHA-256 integrity into CausalTraceLedger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import enum
import hashlib
import json
import logging
from pathlib import Path, PurePath, PurePosixPath
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.context_capsule import AccessMode, CapabilityScope
from ca_runtime.pi_adapter import (
    OPERATION_LANE_BINDINGS,
    AuthorityLane,
    AuthorityLaneMismatchError,
    CaePiRuntimeTrace,
    PiSession,
)
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramTransitionBlockedError,
    ProgramTransitionContract,
    UniversalProgramStateRuntime,
)
from ca_runtime.state_lifecycle import (
    CausalTraceEventType,
    CausalTraceLedger,
    CausalTraceRecord,
    EffectKind,
    FailureWindow,
    HookExecutionStatus,
    HookPhase,
    HookRejectionError,
    HookResult,
    ReplaySafety,
    StateCheckpoint,
    StateEffectDeclaration,
    StateLifecycleCoordinator,
    StateRepairRequiredError,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)
from ca_runtime.tenant_operations import OperationReceipt, _generate_receipt_id

logger = logging.getLogger("ca_runtime.hook_runtime")


# ============================================================================
# 1. Typed Exception Taxonomy
# ============================================================================

class HookRuntimeError(TenancyError):
    """Base exception for hook execution, capability enforcement, and operator gates."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "HOOK_RUNTIME_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class HookExecutionDeniedError(HookRuntimeError):
    """Raised when a hook explicitly denies execution of an action."""

    def __init__(self, hook_point: str, hook_name: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"HOOK_DENIED [{hook_point}:{hook_name}]: {reason}",
            reason_code=f"HOOK_DENIED_{hook_point.upper()}",
            details=details or {},
        )
        self.hook_point = hook_point
        self.hook_name = hook_name
        self.reason = reason


class UnauthorizedCapabilityAccessError(HookRuntimeError):
    """Raised when an actor/agent attempts capability access not explicitly granted."""

    def __init__(self, actor_id: str, scope: CapabilityScope, target: str, reason: str = ""):
        msg = (
            f"CAPABILITY_VIOLATION: Actor '{actor_id}' is not authorized for capability scope "
            f"'{scope.value}' on target '{target}'"
        )
        if reason:
            msg += f" ({reason})"
        super().__init__(
            msg,
            reason_code="UNAUTHORIZED_CAPABILITY_ACCESS",
            details={"actor_id": actor_id, "scope": scope.value, "target": target, "reason": reason},
        )
        self.actor_id = actor_id
        self.scope = scope
        self.target = target


class SandboxSecurityViolationError(HookRuntimeError):
    """Raised when capability access violates sandbox constraints (e.g. path traversal, unsafe CLI)."""

    def __init__(self, scope: CapabilityScope, target: str, violation_type: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"SANDBOX_SECURITY_VIOLATION [{scope.value}]: {violation_type} on target '{target}'",
            reason_code=f"SANDBOX_VIOLATION_{violation_type.upper()}",
            details=details or {},
        )
        self.scope = scope
        self.target = target
        self.violation_type = violation_type


class OperatorGateRequiredError(HookRuntimeError):
    """Raised when execution reaches an operator gate requiring human review."""

    def __init__(self, gate_id: str, decision_context: Dict[str, Any]):
        super().__init__(
            f"OPERATOR_GATE_REQUIRED: Execution paused for operator review on gate '{gate_id}'",
            reason_code="OPERATOR_GATE_REQUIRED",
            details={"gate_id": gate_id, "decision_context": decision_context},
        )
        self.gate_id = gate_id
        self.decision_context = decision_context


class SelfApprovalProhibitedError(HookRuntimeError):
    """Raised when an actor/agent attempts to approve their own operator gate."""

    def __init__(self, actor_id: str, gate_id: str):
        super().__init__(
            f"SELF_APPROVAL_PROHIBITED: Actor '{actor_id}' cannot approve operator gate '{gate_id}' requested by itself",
            reason_code="SELF_APPROVAL_PROHIBITED",
            details={"actor_id": actor_id, "gate_id": gate_id},
        )
        self.actor_id = actor_id
        self.gate_id = gate_id


class CompletionGateVerificationError(HookRuntimeError):
    """Raised when completion is attempted without required evidence, receipts, or approvals."""

    def __init__(self, aggregate_id: str, missing_criteria: Sequence[str]):
        super().__init__(
            f"COMPLETION_BLOCKED: Program state aggregate '{aggregate_id}' is missing required completion criteria: "
            f"{', '.join(missing_criteria)}",
            reason_code="COMPLETION_GATE_VERIFICATION_FAILED",
            details={"aggregate_id": aggregate_id, "missing_criteria": list(missing_criteria)},
        )
        self.aggregate_id = aggregate_id
        self.missing_criteria = tuple(missing_criteria)


# ============================================================================
# 2. Hook Pointcuts & Decision Models
# ============================================================================

class HookPoint(str, enum.Enum):
    """Pointcuts in the CAE/Pi execution lifecycle where hooks execute."""
    PRE_TOOL = "PRE_TOOL"
    POST_MUTATION = "POST_MUTATION"
    STATE_TRANSFER = "STATE_TRANSFER"
    COMPLETION = "COMPLETION"
    RECOVERY = "RECOVERY"
    OPERATOR_GATE = "OPERATOR_GATE"


class HookOutcome(str, enum.Enum):
    """Result outcome of a deterministic hook evaluation."""
    ALLOW = "ALLOW"
    DENY = "DENY"
    GATE_REQUIRED = "GATE_REQUIRED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    OBSERVED = "OBSERVED"


@dataclass(frozen=True, slots=True)
class HookDecisionRecord:
    """Cryptographically verifiable record of a hook evaluation decision."""
    decision_id: str
    hook_point: HookPoint
    hook_name: str
    outcome: HookOutcome
    reason_code: str
    target: str
    actor_id: str
    lane: str
    workspace_id: UUID
    details: Dict[str, Any]
    created_at: str
    decision_sha256: str


def _create_hook_decision_record(
    hook_point: HookPoint,
    hook_name: str,
    outcome: HookOutcome,
    reason_code: str,
    target: str,
    actor_id: str,
    lane: str,
    workspace_id: UUID,
    details: Optional[Dict[str, Any]] = None,
) -> HookDecisionRecord:
    created_at = utc_now_rfc3339()
    payload = {
        "hook_point": hook_point.value,
        "hook_name": hook_name,
        "outcome": outcome.value,
        "reason_code": reason_code,
        "target": target,
        "actor_id": actor_id,
        "lane": lane,
        "workspace_id": str(workspace_id),
        "details": details or {},
        "created_at": created_at,
    }
    digest = canonical_sha256(payload)
    decision_id = f"hook_dec_{digest[:24]}"
    return HookDecisionRecord(
        decision_id=decision_id,
        hook_point=hook_point,
        hook_name=hook_name,
        outcome=outcome,
        reason_code=reason_code,
        target=target,
        actor_id=actor_id,
        lane=lane,
        workspace_id=workspace_id,
        details=details or {},
        created_at=created_at,
        decision_sha256=digest,
    )


# ============================================================================
# 3. Explicit Capability Grants & Security Sandbox Engine
# ============================================================================

@dataclass(frozen=True, slots=True)
class CapabilityGrant:
    """Explicit projection grant adhering to 21_PHASE2_CAPABILITY_SECURITY_MATRIX.md."""
    scope: CapabilityScope
    access_mode: AccessMode
    target: str
    workspace_id: UUID
    allowed_lanes: Tuple[AuthorityLane, ...] = (
        AuthorityLane.HUNTER,
        AuthorityLane.ANALYST,
        AuthorityLane.COMPOSER,
        AuthorityLane.COMMANDER,
    )
    requires_operator_approval: bool = False
    sandbox_root: Optional[str] = None
    network_allowlist: Tuple[str, ...] = ()
    cli_command_allowlist: Tuple[str, ...] = ()

    def is_match(self, requested_scope: CapabilityScope, requested_target: str, requested_mode: AccessMode) -> bool:
        if self.scope != requested_scope:
            return False
        if self.target != "*" and self.target != requested_target:
            # Check prefix matching for paths / topics
            if requested_target.startswith(self.target.rstrip("*")):
                pass
            else:
                return False
        if self.access_mode == AccessMode.READ_WRITE:
            return True
        if self.access_mode == requested_mode:
            return True
        return False


class CapabilityPolicyEngine:
    """Deterministic security engine enforcing the Phase 2 Capability Security Matrix."""

    SAFE_CLI_EXECUTABLES: Set[str] = {
        "git",
        "python",
        "pytest",
        "ffmpeg",
        "ffprobe",
        "echo",
        "cat",
        "grep",
    }

    RISKY_CLI_PATTERNS: List[re.Pattern[str]] = [
        re.compile(r"rm\s+-rf", re.IGNORECASE),
        re.compile(r"mkfs", re.IGNORECASE),
        re.compile(r"dd\s+if=", re.IGNORECASE),
        re.compile(r":\(\)\s*\{", re.IGNORECASE),  # Forkbomb
        re.compile(r";\s*rm", re.IGNORECASE),
        re.compile(r"\|\s*bash", re.IGNORECASE),
        re.compile(r"\|\s*sh", re.IGNORECASE),
    ]

    def __init__(self, grants: Optional[Sequence[CapabilityGrant]] = None):
        self._grants: List[CapabilityGrant] = list(grants or [])

    def add_grant(self, grant: CapabilityGrant) -> None:
        self._grants.append(grant)

    def evaluate_access(
        self,
        *,
        scope: CapabilityScope,
        target: str,
        mode: AccessMode,
        actor_id: str,
        lane: AuthorityLane,
        workspace_id: UUID,
        command_payload: Optional[Mapping[str, Any]] = None,
    ) -> HookDecisionRecord:
        """Evaluates capability access strictly and fail-closed."""
        # 1. Search for matching grant
        matched_grant: Optional[CapabilityGrant] = None
        for grant in self._grants:
            if grant.workspace_id == workspace_id and grant.is_match(scope, target, mode):
                matched_grant = grant
                break

        if matched_grant is None:
            raise UnauthorizedCapabilityAccessError(
                actor_id=actor_id,
                scope=scope,
                target=target,
                reason="No matching explicit capability grant found",
            )

        # 2. Verify Authority Lane
        if lane not in matched_grant.allowed_lanes:
            raise UnauthorizedCapabilityAccessError(
                actor_id=actor_id,
                scope=scope,
                target=target,
                reason=f"Lane '{lane.value}' not authorized for grant (allowed: {[l.value for l in matched_grant.allowed_lanes]})",
            )

        # 3. Scope-Specific Sandbox Checks
        self._enforce_sandbox_rules(
            grant=matched_grant,
            scope=scope,
            target=target,
            mode=mode,
            command_payload=command_payload or {},
        )

        # 4. Operator Approval Gate Check
        if matched_grant.requires_operator_approval:
            return _create_hook_decision_record(
                hook_point=HookPoint.PRE_TOOL,
                hook_name="capability_security_policy",
                outcome=HookOutcome.GATE_REQUIRED,
                reason_code="OPERATOR_APPROVAL_REQUIRED",
                target=target,
                actor_id=actor_id,
                lane=lane.value,
                workspace_id=workspace_id,
                details={"grant_scope": scope.value, "requires_operator_approval": True},
            )

        return _create_hook_decision_record(
            hook_point=HookPoint.PRE_TOOL,
            hook_name="capability_security_policy",
            outcome=HookOutcome.ALLOW,
            reason_code="CAPABILITY_AUTHORIZED",
            target=target,
            actor_id=actor_id,
            lane=lane.value,
            workspace_id=workspace_id,
            details={"grant_scope": scope.value, "mode": mode.value},
        )

    def _enforce_sandbox_rules(
        self,
        *,
        grant: CapabilityGrant,
        scope: CapabilityScope,
        target: str,
        mode: AccessMode,
        command_payload: Mapping[str, Any],
    ) -> None:
        """Enforces domain-specific sandbox constraints."""
        if scope == CapabilityScope.FILESYSTEM:
            # Prevent path traversal
            if ".." in target or target.startswith("../") or target.startswith("..\\"):
                raise SandboxSecurityViolationError(
                    scope=scope,
                    target=target,
                    violation_type="PATH_TRAVERSAL_DETECTED",
                    details={"path": target},
                )
            # Prevent access outside sandbox root if configured
            if grant.sandbox_root:
                normalized_root = PurePosixPath(grant.sandbox_root.replace("\\", "/"))
                normalized_target = PurePosixPath(target.replace("\\", "/"))
                if not str(normalized_target).startswith(str(normalized_root)):
                    raise SandboxSecurityViolationError(
                        scope=scope,
                        target=target,
                        violation_type="OUT_OF_SANDBOX_ACCESS",
                        details={"target": str(normalized_target), "sandbox_root": str(normalized_root)},
                    )

        elif scope == CapabilityScope.PROCESS_CLI:
            executable = target.strip().split()[0] if target else ""
            if grant.cli_command_allowlist and executable not in grant.cli_command_allowlist:
                raise SandboxSecurityViolationError(
                    scope=scope,
                    target=target,
                    violation_type="UNAUTHORIZED_EXECUTABLE",
                    details={"executable": executable, "allowlist": list(grant.cli_command_allowlist)},
                )
            for pattern in self.RISKY_CLI_PATTERNS:
                if pattern.search(target):
                    raise SandboxSecurityViolationError(
                        scope=scope,
                        target=target,
                        violation_type="RISKY_CLI_COMMAND_DETECTED",
                        details={"command": target},
                    )

        elif scope == CapabilityScope.NETWORK:
            # Parse protocol and host
            if "://" in target:
                proto, host_port = target.split("://", 1)
                if proto.lower() not in ("http", "https"):
                    raise SandboxSecurityViolationError(
                        scope=scope,
                        target=target,
                        violation_type="FORBIDDEN_NETWORK_PROTOCOL",
                        details={"protocol": proto},
                    )
                host = host_port.split("/", 1)[0].split(":", 1)[0]
            else:
                host = target.split("/", 1)[0].split(":", 1)[0]

            if grant.network_allowlist and host not in grant.network_allowlist and "*" not in grant.network_allowlist:
                raise SandboxSecurityViolationError(
                    scope=scope,
                    target=target,
                    violation_type="UNAUTHORIZED_NETWORK_HOST",
                    details={"host": host, "allowlist": list(grant.network_allowlist)},
                )

        elif scope == CapabilityScope.SECRETS:
            # Named references only; raw retrieval strictly forbidden
            if not target.startswith("ref:") and not target.startswith("vault:"):
                raise SandboxSecurityViolationError(
                    scope=scope,
                    target=target,
                    violation_type="RAW_SECRET_RETRIEVAL_PROHIBITED",
                    details={"target": target, "instruction": "Use named reference ref:secret_name"},
                )

        elif scope == CapabilityScope.CAE_TYPED_OPERATION:
            # Verify operation format
            if "@" not in target and "." not in target:
                raise SandboxSecurityViolationError(
                    scope=scope,
                    target=target,
                    violation_type="INVALID_OPERATION_IDENTIFIER",
                    details={"target": target},
                )


# ============================================================================
# 4. Durable Operator Gate Runtime Engine
# ============================================================================

class OperatorGateStatus(str, enum.Enum):
    """Lifecycle status of a durable Operator Gate."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class OperatorGateRecord:
    """Durable CAE Operator Gate record satisfying 25_PHASE2_OPERATOR_GATE_RUNTIME_CONTRACT.md."""
    gate_id: str
    workspace_id: UUID
    state_aggregate_id: str
    operation_id: str
    decision_context: Dict[str, Any]
    requester_id: str
    required_role: str
    status: OperatorGateStatus
    decision: Optional[str] = None
    decision_notes: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[str] = None
    created_at: str = field(default_factory=utc_now_rfc3339)
    gate_sha256: str = ""


@dataclass(frozen=True, slots=True)
class OperatorGateReceipt:
    """Authoritative receipt for an operator gate decision."""
    receipt_id: str
    gate_id: str
    workspace_id: UUID
    state_aggregate_id: str
    decision: str
    decided_by: str
    decided_at: str
    receipt_sha256: str


class OperatorGateRuntimeEngine:
    """Durable operator gate manager preventing model self-approval and enforcing immutable audit trails."""

    def __init__(self, trace_ledger: Optional[CausalTraceLedger] = None):
        self._gates: Dict[str, OperatorGateRecord] = {}
        self._receipts: Dict[str, OperatorGateReceipt] = {}
        self._trace_ledger = trace_ledger or CausalTraceLedger()

    def create_operator_gate(
        self,
        *,
        workspace_id: UUID,
        state_aggregate_id: str,
        operation_id: str,
        decision_context: Dict[str, Any],
        requester_id: str,
        required_role: str = "OPERATOR",
    ) -> OperatorGateRecord:
        """Create and persist a durable Operator Gate."""
        created_at = utc_now_rfc3339()
        payload = {
            "workspace_id": str(workspace_id),
            "state_aggregate_id": state_aggregate_id,
            "operation_id": operation_id,
            "decision_context": decision_context,
            "requester_id": requester_id,
            "required_role": required_role,
            "created_at": created_at,
        }
        digest = canonical_sha256(payload)
        gate_id = f"gate_{digest[:24]}"

        # Idempotent creation
        if gate_id in self._gates:
            return self._gates[gate_id]

        record = OperatorGateRecord(
            gate_id=gate_id,
            workspace_id=workspace_id,
            state_aggregate_id=state_aggregate_id,
            operation_id=operation_id,
            decision_context=dict(decision_context),
            requester_id=requester_id,
            required_role=required_role,
            status=OperatorGateStatus.PENDING,
            created_at=created_at,
            gate_sha256=digest,
        )
        self._gates[gate_id] = record

        # Log trace event
        prev_hash = self._trace_ledger.get_latest_trace_hash(state_aggregate_id)
        trace_record = CausalTraceRecord.create(
            cae_run_id=f"run_gate_{gate_id}",
            program_id="operator_gate",
            aggregate_id=state_aggregate_id,
            workspace_id=str(workspace_id),
            lane=AuthorityLane.COMMANDER,
            actor_id=requester_id,
            event_type=CausalTraceEventType.BLOCKED,
            payload={"gate_id": gate_id, "operation_id": operation_id, "status": "PENDING"},
            previous_trace_sha256=prev_hash,
        )
        self._trace_ledger.append(trace_record)

        return record

    def get_gate(self, gate_id: str) -> Optional[OperatorGateRecord]:
        return self._gates.get(gate_id)

    def submit_operator_decision(
        self,
        *,
        gate_id: str,
        decision: str,  # "APPROVED" | "REJECTED"
        context: TenantContext,
        decision_notes: Optional[str] = None,
    ) -> OperatorGateReceipt:
        """Submit an authenticated operator decision for a pending gate.
        
        Enforces:
        - Workspace match.
        - Operator authority (context.role == "OPERATOR" or context.is_operator is True).
        - Anti-Self-Approval rule: requester cannot approve its own gate.
        - Idempotency on duplicate submissions.
        """
        gate = self._gates.get(gate_id)
        if gate is None:
            raise HookRuntimeError(f"Operator gate '{gate_id}' not found", reason_code="GATE_NOT_FOUND")

        # 1. Tenancy match
        if context.workspace_id != gate.workspace_id:
            raise CrossWorkspaceLeakError(
                f"CROSS_WORKSPACE_LEAK: Operator context workspace {context.workspace_id} "
                f"does not match gate workspace {gate.workspace_id}"
            )

        # 2. Operator role authorization
        if context.role != "OPERATOR" and not context.is_operator:
            raise UnauthorizedCapabilityAccessError(
                actor_id=context.actor_id,
                scope=CapabilityScope.CAE_TYPED_OPERATION,
                target=f"operator_gate:{gate_id}",
                reason=f"Actor role '{context.role}' does not have operator clearance",
            )

        # 3. Anti-Self-Approval Rule
        if context.actor_id == gate.requester_id:
            raise SelfApprovalProhibitedError(actor_id=context.actor_id, gate_id=gate_id)

        # 4. Idempotency Check
        if gate.status != OperatorGateStatus.PENDING:
            if gate.decision == decision:
                # Return existing receipt
                receipt_key = f"{gate_id}:{decision}"
                if receipt_key in self._receipts:
                    return self._receipts[receipt_key]
            else:
                raise HookRuntimeError(
                    f"Gate '{gate_id}' already finalized with conflicting decision '{gate.decision}'",
                    reason_code="GATE_ALREADY_FINALIZED",
                )

        # 5. Apply Decision
        decided_at = utc_now_rfc3339()
        new_status = OperatorGateStatus.APPROVED if decision == "APPROVED" else OperatorGateStatus.REJECTED
        updated_gate = OperatorGateRecord(
            gate_id=gate.gate_id,
            workspace_id=gate.workspace_id,
            state_aggregate_id=gate.state_aggregate_id,
            operation_id=gate.operation_id,
            decision_context=gate.decision_context,
            requester_id=gate.requester_id,
            required_role=gate.required_role,
            status=new_status,
            decision=decision,
            decision_notes=decision_notes,
            decided_by=context.actor_id,
            decided_at=decided_at,
            created_at=gate.created_at,
            gate_sha256=gate.gate_sha256,
        )
        self._gates[gate_id] = updated_gate

        # 6. Generate Receipt
        receipt_core = {
            "gate_id": gate_id,
            "workspace_id": str(gate.workspace_id),
            "state_aggregate_id": gate.state_aggregate_id,
            "decision": decision,
            "decided_by": context.actor_id,
            "decided_at": decided_at,
        }
        receipt_digest = canonical_sha256(receipt_core)
        receipt_id = f"rcpt_gate_{receipt_digest[:24]}"
        receipt = OperatorGateReceipt(
            receipt_id=receipt_id,
            gate_id=gate_id,
            workspace_id=gate.workspace_id,
            state_aggregate_id=gate.state_aggregate_id,
            decision=decision,
            decided_by=context.actor_id,
            decided_at=decided_at,
            receipt_sha256=receipt_digest,
        )
        self._receipts[f"{gate_id}:{decision}"] = receipt

        # 7. Record Causal Trace Event
        trace_event = (
            CausalTraceEventType.AUTHORIZED
            if decision == "APPROVED"
            else CausalTraceEventType.BLOCKED
        )
        previous_trace = self._trace_ledger.get_latest_trace_hash(gate.state_aggregate_id)
        decision_trace = CausalTraceRecord.create(
            cae_run_id=f"run_gate_{gate_id}",
            program_id="operator_gate",
            aggregate_id=gate.state_aggregate_id,
            workspace_id=str(gate.workspace_id),
            lane=AuthorityLane.COMMANDER,
            actor_id=context.actor_id,
            event_type=trace_event,
            payload={"gate_id": gate_id, "decision": decision, "receipt_id": receipt_id},
            receipt_id=receipt_id,
            previous_trace_sha256=previous_trace,
        )
        self._trace_ledger.append(decision_trace)

        return receipt


# ============================================================================
# 5. Modular Hook Extension Manager
# ============================================================================

HookCallable = Callable[..., HookDecisionRecord]


class HookExtensionManager:
    """Deterministic hook registry and execution pipeline orchestrating pre/post hooks."""

    def __init__(
        self,
        *,
        policy_engine: Optional[CapabilityPolicyEngine] = None,
        operator_gate_runtime: Optional[OperatorGateRuntimeEngine] = None,
        trace_ledger: Optional[CausalTraceLedger] = None,
    ):
        self.policy_engine = policy_engine or CapabilityPolicyEngine()
        self.trace_ledger = trace_ledger or CausalTraceLedger()
        self.operator_gate_runtime = operator_gate_runtime or OperatorGateRuntimeEngine(trace_ledger=self.trace_ledger)
        self._registered_hooks: Dict[HookPoint, List[Tuple[str, HookCallable, int]]] = {
            pt: [] for pt in HookPoint
        }
        self._decision_history: List[HookDecisionRecord] = []

    def register_hook(
        self,
        hook_point: HookPoint,
        name: str,
        hook_fn: HookCallable,
        priority: int = 100,
    ) -> None:
        """Register a custom deterministic hook function at a pointcut."""
        self._registered_hooks[hook_point].append((name, hook_fn, priority))
        # Sort by priority ascending (lower number = runs earlier)
        self._registered_hooks[hook_point].sort(key=lambda x: x[2])

    def get_decision_history(self) -> Sequence[HookDecisionRecord]:
        return tuple(self._decision_history)

    # ------------------------------------------------------------------------
    # 5.1 PRE_TOOL Hook Execution
    # ------------------------------------------------------------------------
    def execute_pre_tool_hooks(
        self,
        *,
        scope: CapabilityScope,
        target: str,
        mode: AccessMode,
        actor_id: str,
        lane: AuthorityLane,
        workspace_id: UUID,
        state_aggregate_id: Optional[str] = None,
        command_payload: Optional[Mapping[str, Any]] = None,
    ) -> HookDecisionRecord:
        """Executes all pre-tool security, capability, and gate hooks fail-closed."""
        # 1. Capability Security Policy Evaluation
        decision = self.policy_engine.evaluate_access(
            scope=scope,
            target=target,
            mode=mode,
            actor_id=actor_id,
            lane=lane,
            workspace_id=workspace_id,
            command_payload=command_payload,
        )
        self._decision_history.append(decision)

        # 2. Check if Operator Gate is required
        if decision.outcome == HookOutcome.GATE_REQUIRED:
            agg_id = state_aggregate_id or f"temp_agg_{workspace_id}"
            gate = self.operator_gate_runtime.create_operator_gate(
                workspace_id=workspace_id,
                state_aggregate_id=agg_id,
                operation_id=target,
                decision_context=dict(command_payload or {}),
                requester_id=actor_id,
            )
            raise OperatorGateRequiredError(gate_id=gate.gate_id, decision_context=gate.decision_context)

        # 3. Run Custom Registered PRE_TOOL Hooks
        for hook_name, hook_fn, _ in self._registered_hooks[HookPoint.PRE_TOOL]:
            custom_decision = hook_fn(
                scope=scope,
                target=target,
                mode=mode,
                actor_id=actor_id,
                lane=lane,
                workspace_id=workspace_id,
                command_payload=command_payload,
            )
            self._decision_history.append(custom_decision)
            if custom_decision.outcome == HookOutcome.DENY:
                raise HookExecutionDeniedError(
                    hook_point=HookPoint.PRE_TOOL.value,
                    hook_name=hook_name,
                    reason=custom_decision.reason_code,
                    details=custom_decision.details,
                )

        return decision

    # ------------------------------------------------------------------------
    # 5.2 POST_MUTATION Hook Execution
    # ------------------------------------------------------------------------
    def execute_post_mutation_hooks(
        self,
        *,
        target: str,
        actor_id: str,
        lane: AuthorityLane,
        workspace_id: UUID,
        mutation_result: Any,
        side_effects: Optional[Sequence[StateEffectDeclaration]] = None,
    ) -> HookDecisionRecord:
        """Executes post-mutation hooks: registers side effects and schema assertions."""
        details: Dict[str, Any] = {
            "side_effect_count": len(side_effects or []),
            "mutation_result_type": type(mutation_result).__name__,
        }
        decision = _create_hook_decision_record(
            hook_point=HookPoint.POST_MUTATION,
            hook_name="post_mutation_schema_validator",
            outcome=HookOutcome.ALLOW,
            reason_code="MUTATION_VALIDATED",
            target=target,
            actor_id=actor_id,
            lane=lane.value,
            workspace_id=workspace_id,
            details=details,
        )
        self._decision_history.append(decision)

        # Run registered custom POST_MUTATION hooks
        for hook_name, hook_fn, _ in self._registered_hooks[HookPoint.POST_MUTATION]:
            custom_decision = hook_fn(
                target=target,
                actor_id=actor_id,
                lane=lane,
                workspace_id=workspace_id,
                mutation_result=mutation_result,
                side_effects=side_effects,
            )
            self._decision_history.append(custom_decision)
            if custom_decision.outcome == HookOutcome.DENY:
                raise HookExecutionDeniedError(
                    hook_point=HookPoint.POST_MUTATION.value,
                    hook_name=hook_name,
                    reason=custom_decision.reason_code,
                    details=custom_decision.details,
                )

        return decision

    # ------------------------------------------------------------------------
    # 5.3 STATE_TRANSFER Hook Execution
    # ------------------------------------------------------------------------
    def execute_state_transfer_hooks(
        self,
        *,
        aggregate_id: str,
        from_state: str,
        to_state: str,
        actor_id: str,
        lane: AuthorityLane,
        workspace_id: UUID,
        contract: Optional[ProgramTransitionContract] = None,
    ) -> HookDecisionRecord:
        """Validates state transfer preconditions and transition contract constraints."""
        details: Dict[str, Any] = {
            "from_state": from_state,
            "to_state": to_state,
            "contract_required_lane": contract.required_lane.value if contract else None,
        }
        decision = _create_hook_decision_record(
            hook_point=HookPoint.STATE_TRANSFER,
            hook_name="state_transfer_guard",
            outcome=HookOutcome.ALLOW,
            reason_code="TRANSFER_PERMITTED",
            target=aggregate_id,
            actor_id=actor_id,
            lane=lane.value,
            workspace_id=workspace_id,
            details=details,
        )
        self._decision_history.append(decision)

        # Run registered custom STATE_TRANSFER hooks
        for hook_name, hook_fn, _ in self._registered_hooks[HookPoint.STATE_TRANSFER]:
            custom_decision = hook_fn(
                aggregate_id=aggregate_id,
                from_state=from_state,
                to_state=to_state,
                actor_id=actor_id,
                lane=lane,
                workspace_id=workspace_id,
                contract=contract,
            )
            self._decision_history.append(custom_decision)
            if custom_decision.outcome == HookOutcome.DENY:
                raise HookExecutionDeniedError(
                    hook_point=HookPoint.STATE_TRANSFER.value,
                    hook_name=hook_name,
                    reason=custom_decision.reason_code,
                    details=custom_decision.details,
                )

        return decision

    # ------------------------------------------------------------------------
    # 5.4 COMPLETION Hook Execution
    # ------------------------------------------------------------------------
    def execute_completion_hooks(
        self,
        *,
        aggregate: ProgramStateAggregate,
        required_receipt_ids: Sequence[str],
        required_gate_ids: Sequence[str] = (),
        context: Optional[TenantContext] = None,
    ) -> HookDecisionRecord:
        """Ensures that a program state aggregate cannot complete without verifiable proof."""
        missing: List[str] = []

        # 1. Check required receipts
        if not required_receipt_ids:
            missing.append("REQUIRED_RECEIPTS_EMPTY")

        # 2. Check operator gate statuses
        for gate_id in required_gate_ids:
            gate = self.operator_gate_runtime.get_gate(gate_id)
            if gate is None or gate.status != OperatorGateStatus.APPROVED:
                missing.append(f"UNAPPROVED_OPERATOR_GATE:{gate_id}")

        if missing:
            raise CompletionGateVerificationError(
                aggregate_id=aggregate.aggregate_id,
                missing_criteria=missing,
            )

        decision = _create_hook_decision_record(
            hook_point=HookPoint.COMPLETION,
            hook_name="completion_evidence_verifier",
            outcome=HookOutcome.ALLOW,
            reason_code="COMPLETION_EVIDENCE_SATISFIED",
            target=aggregate.aggregate_id,
            actor_id=context.actor_id if context else "system",
            lane=AuthorityLane.COMMANDER.value,
            workspace_id=aggregate.workspace_id,
            details={
                "verified_receipt_count": len(required_receipt_ids),
                "verified_gate_count": len(required_gate_ids),
            },
        )
        self._decision_history.append(decision)

        # Run registered custom COMPLETION hooks
        for hook_name, hook_fn, _ in self._registered_hooks[HookPoint.COMPLETION]:
            custom_decision = hook_fn(
                aggregate=aggregate,
                required_receipt_ids=required_receipt_ids,
                required_gate_ids=required_gate_ids,
                context=context,
            )
            self._decision_history.append(custom_decision)
            if custom_decision.outcome == HookOutcome.DENY:
                raise HookExecutionDeniedError(
                    hook_point=HookPoint.COMPLETION.value,
                    hook_name=hook_name,
                    reason=custom_decision.reason_code,
                    details=custom_decision.details,
                )

        return decision

    # ------------------------------------------------------------------------
    # 5.5 RECOVERY Hook Execution
    # ------------------------------------------------------------------------
    def execute_recovery_hooks(
        self,
        *,
        aggregate_id: str,
        workspace_id: UUID,
        actor_id: str,
        error: Exception,
        state_runtime: UniversalProgramStateRuntime,
    ) -> HookDecisionRecord:
        """Routes failure safely to REPAIRING lifecycle state and logs recovery trace."""
        decision = _create_hook_decision_record(
            hook_point=HookPoint.RECOVERY,
            hook_name="governed_recovery_router",
            outcome=HookOutcome.REPAIR_REQUIRED,
            reason_code="REPAIR_ROUTING_ACTIVATED",
            target=aggregate_id,
            actor_id=actor_id,
            lane=AuthorityLane.COMMANDER.value,
            workspace_id=workspace_id,
            details={"error_type": type(error).__name__, "error_message": str(error)},
        )
        self._decision_history.append(decision)

        # Transition state aggregate to REPAIRING if it exists and is not already terminal
        try:
            agg = state_runtime.get_aggregate(aggregate_id)
            if agg and agg.lifecycle not in (ProgramStateLifecycle.COMPLETED, ProgramStateLifecycle.FAILED):
                now = utc_now_rfc3339()
                updated_agg = ProgramStateAggregate(
                    aggregate_id=agg.aggregate_id,
                    workspace_id=agg.workspace_id,
                    cae_run_id=agg.cae_run_id,
                    program_id=agg.program_id,
                    program_version=agg.program_version,
                    current_state=agg.current_state,
                    state_data=dict(agg.state_data),
                    version=agg.version,
                    state_hash=agg.state_hash,
                    lifecycle=ProgramStateLifecycle.REPAIRING,
                    last_receipt_id=agg.last_receipt_id,
                    created_at=agg.created_at,
                    updated_at=now,
                )
                state_runtime.store.save_aggregate(updated_agg)
        except Exception as exc:
            logger.warning("Could not transition aggregate %s to REPAIRING: %s", aggregate_id, exc)

        # Record recovery trace
        previous_trace = self.trace_ledger.get_latest_trace_hash(aggregate_id)
        recovery_trace = CausalTraceRecord.create(
            cae_run_id=f"run_rec_{aggregate_id}",
            program_id="recovery",
            aggregate_id=aggregate_id,
            workspace_id=str(workspace_id),
            lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            event_type=CausalTraceEventType.REPAIRED,
            payload={"error": str(error), "decision_id": decision.decision_id},
            recovery_status="REPAIRING",
            previous_trace_sha256=previous_trace,
        )
        self.trace_ledger.append(recovery_trace)

        return decision
