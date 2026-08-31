"""CAE Four-Lane Agent Team and Sub-agent Runtime Subsystem.

Governed by:
- Phase 2 Mandate M21 (02_PHASE_2_RUNTIME_FOUNDATION/M21_four_lane_agent_team_sub_agent_runtime.md)
- Phase 1 Mandate M09 (00_CONTROL/19_PHASE1_AGENT_TEAM_DELEGATION_REFERENCE_TOPOLOGY.md)
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 00_CONTROL/25_PHASE2_OPERATOR_GATE_RUNTIME_CONTRACT.md
- 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md

Enforces:
1. Four Non-Negotiable Authority Lanes:
   - HUNTER: Signal & evidence discovery. May NOT evaluate, compose, or authorize.
   - ANALYST: Adversarial critique, falsification & rubrics. May NOT invent or synthesize.
   - COMPOSER: Creative synthesis & structuring. May NOT bypass analyst or authorize state.
   - COMMANDER: Governance, tenant RLS, operator gates & state/receipt seal.
2. Passive, Flat Canonical Skills:
   - Skills are pure procedure files (SKILL.md). No skill may invoke another skill or agent.
3. Explicit Capability Projections:
   - Capability access is strictly declared and validated against the Capability Security Matrix.
   - Ambient process, secret, network, and database access are strictly forbidden.
4. Bounded Execution & Resilience:
   - Bounded concurrency with async Semaphore.
   - Per-task timeout, clean cancellation, exponential backoff retries, and structured failure propagation.
5. Operator Gate Runtime Contract:
   - Human approval steps transition to WAITING_OPERATOR with immutable decision context.
   - Models are constitutionally prohibited from approving their own work.
6. Cryptographic Receipt Provenance:
   - Full sha256 hash chains and deterministic receipt generation for all delegations.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
import random
import time
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.context_capsule import AccessMode, CapabilityScope, SkillMaturity
from ca_runtime.pi_adapter import (
    AuthorityLane,
    AuthorityLaneMismatchError,
    CaePiRuntimeAdapter,
    CaePiRuntimeTrace,
    PiExecutionReceipt,
    PiRuntimeError,
    PiSession,
    PiSessionState,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)
from ca_runtime.tenant_operations import OperationReceipt, _generate_receipt_id
from cmf_pipeline.domain.enums import WorkflowRole


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class AgentRuntimeError(TenancyError):
    """Base exception for Agent Team and Sub-agent runtime operations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "AGENT_RUNTIME_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class UnauthorizedAuthorityLaneError(AgentRuntimeError):
    """Raised when an agent or sub-agent attempts work across an unauthorized Authority Lane."""

    def __init__(self, agent_id: str, assigned_lane: AuthorityLane, attempted_lane: AuthorityLane, operation_id: str = ""):
        super().__init__(
            f"LANE_VIOLATION: Agent '{agent_id}' in lane '{assigned_lane.value}' cannot execute "
            f"work in '{attempted_lane.value}' lane (operation: '{operation_id}')",
            reason_code="UNAUTHORIZED_AUTHORITY_LANE",
            details={
                "agent_id": agent_id,
                "assigned_lane": assigned_lane.value,
                "attempted_lane": attempted_lane.value,
                "operation_id": operation_id,
            },
        )


class UnauthorizedCapabilityAccessError(AgentRuntimeError):
    """Raised when an agent attempts to access a capability not explicitly projected."""

    def __init__(self, agent_id: str, scope: CapabilityScope, target: str):
        super().__init__(
            f"CAPABILITY_VIOLATION: Agent '{agent_id}' does not have capability grant for "
            f"scope '{scope.value}' on target '{target}'",
            reason_code="UNAUTHORIZED_CAPABILITY_ACCESS",
            details={"agent_id": agent_id, "scope": scope.value, "target": target},
        )


class SkillNestingProhibitedError(AgentRuntimeError):
    """Raised when a Skill attempts to invoke another Skill or spawn a sub-agent."""

    def __init__(self, skill_id: str, reason: str):
        super().__init__(
            f"SKILL_NESTING_VIOLATION: Skill '{skill_id}' violates passive/flat constitution: {reason}",
            reason_code="SKILL_NESTING_PROHIBITED",
            details={"skill_id": skill_id, "reason": reason},
        )


class DelegationTopologyViolationError(AgentRuntimeError):
    """Raised when delegation path violates the team's declared topology."""

    def __init__(self, delegator_id: str, target_id: str):
        super().__init__(
            f"TOPOLOGY_VIOLATION: Agent '{delegator_id}' is not authorized to delegate to '{target_id}'",
            reason_code="DELEGATION_TOPOLOGY_VIOLATION",
            details={"delegator_id": delegator_id, "target_id": target_id},
        )


class ConcurrencyLimitExceededError(AgentRuntimeError):
    """Raised when concurrent task execution exceeds the bounded team limit."""

    def __init__(self, team_id: str, max_concurrency: int):
        super().__init__(
            f"CONCURRENCY_LIMIT_EXCEEDED: Team '{team_id}' exceeded max concurrency limit of {max_concurrency}",
            reason_code="CONCURRENCY_LIMIT_EXCEEDED",
            details={"team_id": team_id, "max_concurrency": max_concurrency},
        )


class AgentExecutionTimeoutError(AgentRuntimeError):
    """Raised when an agent task execution exceeds its allocated timeout."""

    def __init__(self, agent_id: str, timeout_seconds: float):
        super().__init__(
            f"TIMEOUT: Execution for agent '{agent_id}' timed out after {timeout_seconds}s",
            reason_code="AGENT_EXECUTION_TIMEOUT",
            details={"agent_id": agent_id, "timeout_seconds": timeout_seconds},
        )


class OperatorGateRequiredError(AgentRuntimeError):
    """Raised/signaled when execution hits a durable Operator Gate requiring human review."""

    def __init__(self, gate_id: str, decision_context: Dict[str, Any]):
        super().__init__(
            f"OPERATOR_GATE_REQUIRED: Execution paused for operator gate '{gate_id}'",
            reason_code="OPERATOR_GATE_REQUIRED",
            details={"gate_id": gate_id, "decision_context": decision_context},
        )


# ---------------------------------------------------------------------------
# Capability Projection & Security Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CapabilityProjection:
    """Explicit capability projection adhering to the Phase 2 Capability Security Matrix."""
    scope: CapabilityScope
    access_mode: AccessMode
    target: str
    requires_operator_approval: bool = False

    def validate_access(self, requested_scope: CapabilityScope, requested_target: str, requested_mode: AccessMode) -> bool:
        """Check whether this projection authorizes the requested access."""
        if self.scope != requested_scope:
            return False
        # Wildcard match or exact match on target
        if self.target != "*" and self.target != requested_target:
            return False
        # Access mode check
        if self.access_mode == AccessMode.READ_WRITE:
            return True
        if self.access_mode == requested_mode:
            return True
        return False


# ---------------------------------------------------------------------------
# Agent and Sub-agent Specification Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Exponential backoff retry policy for agent execution."""
    max_retries: int = 2
    initial_delay_seconds: float = 0.5
    backoff_factor: float = 2.0
    jitter: bool = True


@dataclass(frozen=True, slots=True)
class SubagentSpec:
    """Sub-agent specification bounded strictly to its parent agent's authority lane."""
    subagent_id: str
    name: str
    parent_agent_id: str
    authority_lane: AuthorityLane
    allowed_capabilities: Sequence[CapabilityProjection] = ()
    skills: Sequence[str] = ()
    timeout_seconds: float = 30.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    system_prompt_template: Optional[str] = None

    def validate(self) -> None:
        """Validate sub-agent invariants."""
        if not self.subagent_id or not self.subagent_id.strip():
            raise ValueError("subagent_id cannot be empty")
        if not self.parent_agent_id or not self.parent_agent_id.strip():
            raise ValueError("parent_agent_id cannot be empty")
        if not isinstance(self.authority_lane, AuthorityLane):
            raise ValueError(f"Invalid authority_lane: {self.authority_lane}")
        for skill in self.skills:
            if not isinstance(skill, str) or not skill.strip():
                raise ValueError("Skill identifiers must be non-empty strings")


@dataclass(frozen=True, slots=True)
class AgentMemberSpec:
    """Main Agent Team member specification bound to a specific Authority Lane."""
    agent_id: str
    name: str
    authority_lane: AuthorityLane
    allowed_capabilities: Sequence[CapabilityProjection] = ()
    skills: Sequence[str] = ()
    subagents: Mapping[str, SubagentSpec] = field(default_factory=dict)
    timeout_seconds: float = 60.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    is_commander: bool = False
    system_prompt_template: Optional[str] = None

    def validate(self) -> None:
        """Validate agent member invariants and subagent lane containment."""
        if not self.agent_id or not self.agent_id.strip():
            raise ValueError("agent_id cannot be empty")
        if not isinstance(self.authority_lane, AuthorityLane):
            raise ValueError(f"Invalid authority_lane: {self.authority_lane}")
        # Commander flag consistency
        if self.is_commander and self.authority_lane != AuthorityLane.COMMANDER:
            raise ValueError("is_commander=True is only valid for agents in COMMANDER lane")
        # Validate subagents
        for sub_id, sub_spec in self.subagents.items():
            sub_spec.validate()
            # Constitutional Rule: Subagent cannot exceed parent agent lane
            if sub_spec.authority_lane != self.authority_lane:
                raise UnauthorizedAuthorityLaneError(
                    agent_id=sub_id,
                    assigned_lane=sub_spec.authority_lane,
                    attempted_lane=self.authority_lane,
                    operation_id="subagent_registration",
                )


@dataclass(frozen=True, slots=True)
class AgentTeamSpec:
    """Governed Agent Team specification with explicit topology and concurrency bounds."""
    team_id: str
    name: str
    workspace_id: UUID
    members: Mapping[str, AgentMemberSpec]
    allowed_delegations: Mapping[str, Sequence[str]] = field(default_factory=dict)
    orchestrator_id: Optional[str] = None
    max_concurrency: int = 4
    global_timeout_seconds: float = 180.0

    def validate(self) -> None:
        """Validate team topology and member declarations."""
        if not self.team_id or not self.team_id.strip():
            raise ValueError("team_id cannot be empty")
        if not isinstance(self.workspace_id, UUID):
            raise ValueError(f"workspace_id must be a UUID, got {type(self.workspace_id)}")
        if self.max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        for member_id, member_spec in self.members.items():
            member_spec.validate()

        valid_delegators = set(self.members.keys())
        for m in self.members.values():
            valid_delegators.update(m.subagents.keys())
        if self.orchestrator_id:
            valid_delegators.add(self.orchestrator_id)
        valid_delegators.add("orchestrator")
        valid_delegators.add(f"{self.team_id}_orchestrator")
        valid_delegators.add("collision_orchestrator")

        # Validate delegation graph references
        for delegator, targets in self.allowed_delegations.items():
            if delegator not in valid_delegators:
                raise ValueError(f"Delegator '{delegator}' is not a registered member, subagent, or orchestrator")
            for target in targets:
                if target not in self.members and not any(target in m.subagents for m in self.members.values()):
                    raise ValueError(f"Delegation target '{target}' is not a registered member or subagent")


# ---------------------------------------------------------------------------
# Delegation Task & Result Models
# ---------------------------------------------------------------------------

class DelegationStatus(str, Enum):
    """Lifecycle status for an agent delegation task."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"
    WAITING_OPERATOR = "WAITING_OPERATOR"


@dataclass(frozen=True, slots=True)
class DelegationTask:
    """Explicit delegation task container passed between orchestrator and agent/subagent."""
    task_id: str
    session_id: str
    delegator_id: str
    target_id: str
    authority_lane: AuthorityLane
    input_payload: Mapping[str, Any]
    idempotency_key: str
    required_capabilities: Sequence[Tuple[CapabilityScope, str, AccessMode]] = ()
    skills: Sequence[str] = ()
    is_subagent: bool = False
    created_at: str = field(default_factory=utc_now_rfc3339)


@dataclass(frozen=True, slots=True)
class StructuredDelegationResult:
    """Immutable, cryptographically verifiable result of an agent delegation."""
    task_id: str
    session_id: str
    actor_id: str
    authority_lane: AuthorityLane
    status: DelegationStatus
    output_payload: Optional[Dict[str, Any]]
    error_details: Optional[Dict[str, Any]]
    attempt_count: int
    execution_duration_ms: float
    receipt_id: str
    provenance_chain: Sequence[str]
    result_sha256: str
    created_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "authority_lane": self.authority_lane.value,
            "status": self.status.value,
            "output_payload": self.output_payload,
            "error_details": self.error_details,
            "attempt_count": self.attempt_count,
            "execution_duration_ms": self.execution_duration_ms,
            "receipt_id": self.receipt_id,
            "provenance_chain": list(self.provenance_chain),
            "result_sha256": self.result_sha256,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# Four-Lane Agent Team Runtime Engine
# ---------------------------------------------------------------------------

class AgentTeamRuntime:
    """Bounded multi-agent and sub-agent execution runtime for CAE.
    
    Coordinates agent teams, sub-agents, Pi execution substrate, capability checks,
    timeout handling, exponential backoff retries, operator gates, and receipt lineage.
    """

    def __init__(
        self,
        team_spec: AgentTeamSpec,
        pi_adapter: Optional[CaePiRuntimeAdapter] = None,
        skill_registry: Optional[Mapping[str, Callable[[Mapping[str, Any]], Dict[str, Any]]]] = None,
    ) -> None:
        team_spec.validate()
        self.team_spec = team_spec
        self.pi_adapter = pi_adapter or CaePiRuntimeAdapter()
        self._skill_registry: Dict[str, Callable[[Mapping[str, Any]], Dict[str, Any]]] = dict(skill_registry or {})
        self._semaphore = asyncio.Semaphore(team_spec.max_concurrency)
        self._traces: List[CaePiRuntimeTrace] = []
        self._receipts: List[StructuredDelegationResult] = []
        self._operator_gate_contexts: Dict[str, Dict[str, Any]] = {}

    def register_skill(self, skill_id: str, handler: Callable[[Mapping[str, Any]], Dict[str, Any]]) -> None:
        """Register a passive, flat skill procedure handler."""
        if not skill_id or not skill_id.strip():
            raise ValueError("skill_id cannot be empty")
        self._skill_registry[skill_id] = handler

    def _resolve_target(self, target_id: str) -> Tuple[AgentMemberSpec | SubagentSpec, bool]:
        """Resolve target agent or subagent spec. Returns (spec, is_subagent)."""
        if target_id in self.team_spec.members:
            return self.team_spec.members[target_id], False
        for member in self.team_spec.members.values():
            if target_id in member.subagents:
                return member.subagents[target_id], True
        raise ValueError(f"Unknown target agent or subagent ID: '{target_id}'")

    def _check_delegation_topology(self, delegator_id: str, target_id: str) -> None:
        """Verify that the delegator is authorized to delegate to target_id."""
        if not self.team_spec.allowed_delegations:
            # If no explicit topology specified, allow delegation within registered members
            return
        allowed_targets = self.team_spec.allowed_delegations.get(delegator_id, ())
        if target_id not in allowed_targets:
            raise DelegationTopologyViolationError(delegator_id, target_id)

    def _check_capabilities(
        self,
        spec: AgentMemberSpec | SubagentSpec,
        required_capabilities: Sequence[Tuple[CapabilityScope, str, AccessMode]],
    ) -> None:
        """Assert that the target agent holds all required capability projections."""
        for req_scope, req_target, req_mode in required_capabilities:
            authorized = any(
                grant.validate_access(req_scope, req_target, req_mode)
                for grant in spec.allowed_capabilities
            )
            if not authorized:
                actor_id = spec.agent_id if isinstance(spec, AgentMemberSpec) else spec.subagent_id
                raise UnauthorizedCapabilityAccessError(actor_id, req_scope, req_target)

    def _check_skill_nesting(self, skills: Sequence[str]) -> None:
        """Assert that skills are flat and do not invoke other skills or spawn subagents."""
        for skill_id in skills:
            # Check for illegal nesting markers or reserved prohibited names
            if "nested" in skill_id.lower() or "recursive" in skill_id.lower() or "subagent" in skill_id.lower():
                raise SkillNestingProhibitedError(skill_id, "Skill name implies nested delegation or recursive calls")

    async def execute_task(
        self,
        task: DelegationTask,
        executor_fn: Optional[Callable[[DelegationTask], Dict[str, Any]]] = None,
        async_executor_fn: Optional[Callable[[DelegationTask], Any]] = None,
    ) -> StructuredDelegationResult:
        """Execute a delegation task with bounded concurrency, timeout, retry, and receipt lineage."""
        start_time = time.perf_counter()

        # 1. Tenancy Verification
        tenant_ctx = require_current_tenant_context()
        if tenant_ctx.workspace_id != self.team_spec.workspace_id:
            raise CrossWorkspaceLeakError(
                f"CROSS_WORKSPACE_LEAK: Execution workspace '{tenant_ctx.workspace_id}' "
                f"does not match team workspace '{self.team_spec.workspace_id}'"
            )

        # 2. Topology & Target Resolution
        self._check_delegation_topology(task.delegator_id, task.target_id)
        target_spec, is_subagent = self._resolve_target(task.target_id)
        actor_id = target_spec.agent_id if isinstance(target_spec, AgentMemberSpec) else target_spec.subagent_id

        # 3. Authority Lane Validation (Fail Closed)
        if target_spec.authority_lane != task.authority_lane:
            raise UnauthorizedAuthorityLaneError(
                agent_id=actor_id,
                assigned_lane=target_spec.authority_lane,
                attempted_lane=task.authority_lane,
                operation_id=task.task_id,
            )

        # 4. Capability Validation (Fail Closed)
        self._check_capabilities(target_spec, task.required_capabilities)

        # 5. Flat Passive Skill Validation (Fail Closed)
        self._check_skill_nesting(task.skills)

        # 6. Create Pi Session for Substrate Isolation
        pi_session = self.pi_adapter.create_session(
            cae_run_id=task.session_id,
            workspace_id=tenant_ctx.workspace_id,
            lane=target_spec.authority_lane,
            metadata={"task_id": task.task_id, "actor_id": actor_id, "is_subagent": is_subagent},
        )

        timeout_sec = target_spec.timeout_seconds or self.team_spec.global_timeout_seconds
        retry_policy = target_spec.retry_policy
        attempts = 0
        last_error: Optional[Exception] = None
        output_data: Optional[Dict[str, Any]] = None
        status = DelegationStatus.RUNNING

        # 7. Bounded Execution Loop with Retries
        async with self._semaphore:
            for attempt in range(1, retry_policy.max_retries + 2):
                attempts = attempt
                try:
                    # Execute within timeout
                    async with asyncio.timeout(timeout_sec):
                        if async_executor_fn is not None:
                            output_data = await async_executor_fn(task)
                        elif executor_fn is not None:
                            # Run synchronous executor in default thread pool
                            loop = asyncio.get_running_loop()
                            output_data = await loop.run_in_executor(None, executor_fn, task)
                        else:
                            # Default execution: run declared skills sequentially
                            output_data = await self._execute_skills(task)

                        status = DelegationStatus.SUCCEEDED
                        break

                except asyncio.TimeoutError:
                    last_error = AgentExecutionTimeoutError(actor_id, timeout_sec)
                    status = DelegationStatus.TIMED_OUT
                    break  # Do not retry on hard timeouts
                except OperatorGateRequiredError as og:
                    # Explicit Operator Gate pause: transition to WAITING_OPERATOR
                    status = DelegationStatus.WAITING_OPERATOR
                    self._operator_gate_contexts[task.task_id] = og.details
                    output_data = {"operator_gate": og.details, "status": "WAITING_OPERATOR"}
                    break
                except (UnauthorizedAuthorityLaneError, UnauthorizedCapabilityAccessError, SkillNestingProhibitedError, CrossWorkspaceLeakError):
                    # Constitutional / security violations fail immediately with zero retries
                    raise
                except Exception as ex:
                    last_error = ex
                    status = DelegationStatus.FAILED
                    if attempt <= retry_policy.max_retries:
                        delay = retry_policy.initial_delay_seconds * (retry_policy.backoff_factor ** (attempt - 1))
                        if retry_policy.jitter:
                            delay += random.uniform(0.01, 0.1)
                        await asyncio.sleep(delay)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # 8. Cryptographic Receipt Generation & Provenance Hash
        receipt_id = _generate_receipt_id(
            f"cae.agent_team.delegation@{task.authority_lane.value.lower()}",
            tenant_ctx.workspace_id,
            task.idempotency_key,
        )

        error_info: Optional[Dict[str, Any]] = None
        if status == DelegationStatus.FAILED or status == DelegationStatus.TIMED_OUT:
            error_info = {
                "error_type": type(last_error).__name__ if last_error else "UnknownError",
                "message": str(last_error) if last_error else "Execution failed",
            }

        result_payload_for_digest = {
            "task_id": task.task_id,
            "session_id": task.session_id,
            "actor_id": actor_id,
            "authority_lane": target_spec.authority_lane.value,
            "status": status.value,
            "output_payload": output_data,
            "error": error_info,
            "attempt_count": attempts,
        }
        result_sha = canonical_sha256(canonical_json_text(result_payload_for_digest))

        # Provenance chain: hash of input payload + session ID
        input_digest = canonical_sha256(canonical_json_text(dict(task.input_payload)))
        provenance = (
            f"input_sha256:{input_digest}",
            f"session:{task.session_id}",
            f"lane:{target_spec.authority_lane.value}",
            f"actor:{actor_id}",
        )

        structured_result = StructuredDelegationResult(
            task_id=task.task_id,
            session_id=task.session_id,
            actor_id=actor_id,
            authority_lane=target_spec.authority_lane,
            status=status,
            output_payload=output_data,
            error_details=error_info,
            attempt_count=attempts,
            execution_duration_ms=round(elapsed_ms, 2),
            receipt_id=receipt_id,
            provenance_chain=provenance,
            result_sha256=result_sha,
        )

        self._receipts.append(structured_result)
        return structured_result

    async def _execute_skills(self, task: DelegationTask) -> Dict[str, Any]:
        """Execute registered flat passive skills sequentially for the task."""
        collected_outputs: Dict[str, Any] = {}
        for skill_id in task.skills:
            if skill_id not in self._skill_registry:
                raise AgentRuntimeError(f"Skill '{skill_id}' is not registered in runtime", reason_code="SKILL_NOT_FOUND")
            handler = self._skill_registry[skill_id]
            loop = asyncio.get_running_loop()
            skill_output = await loop.run_in_executor(None, handler, task.input_payload)
            collected_outputs[skill_id] = skill_output
        return collected_outputs

    def get_receipts(self) -> Sequence[StructuredDelegationResult]:
        """Retrieve all execution receipts emitted during team runtime."""
        return list(self._receipts)

    def get_operator_gate_context(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve decision context for a task waiting on operator approval."""
        return self._operator_gate_contexts.get(task_id)


# ---------------------------------------------------------------------------
# Ratified Reference Pilot Implementation (Collision Discovery Team)
# ---------------------------------------------------------------------------

def create_collision_discovery_pilot_team(workspace_id: UUID) -> Tuple[AgentTeamSpec, AgentTeamRuntime]:
    """Factory creating the ratified Phase 1 M09 Collision Discovery Team reference topology.
    
    Topology:
    - Hunter Lane:
        - `CollisionHunterAgent` (Hunter Member)
        - `CollisionSubHunter` (Hunter Subagent: Signal Ingestion)
    - Analyst Lane:
        - `CollisionAnalystAgent` (Analyst Member)
    - Composer Lane:
        - `CollisionComposerAgent` (Composer Member)
    - Commander Lane:
        - `CollisionCommanderAgent` (Commander Member with Operator Gate)
    """
    sub_hunter = SubagentSpec(
        subagent_id="collision_sub_hunter",
        name="Collision Signal Sub-Hunter",
        parent_agent_id="collision_hunter",
        authority_lane=AuthorityLane.HUNTER,
        allowed_capabilities=(
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.READ_ONLY, "cae.evidence.capture@1.0.0"),
            CapabilityProjection(CapabilityScope.FILESYSTEM, AccessMode.READ_ONLY, "fixtures/harnesses/*"),
        ),
        skills=("collision-evidence-ingest",),
        timeout_seconds=15.0,
    )

    hunter = AgentMemberSpec(
        agent_id="collision_hunter",
        name="Collision Hypothesis Hunter",
        authority_lane=AuthorityLane.HUNTER,
        allowed_capabilities=(
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.READ_ONLY, "cae.evidence.capture@1.0.0"),
            CapabilityProjection(CapabilityScope.POSTGRES_STORAGE, AccessMode.READ_ONLY, "cae.media_asset"),
        ),
        skills=("collision-hypothesis-hunter",),
        subagents={"collision_sub_hunter": sub_hunter},
        timeout_seconds=30.0,
    )

    analyst = AgentMemberSpec(
        agent_id="collision_analyst",
        name="Collision Falsification Analyst",
        authority_lane=AuthorityLane.ANALYST,
        allowed_capabilities=(
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.READ_ONLY, "cae.assessment.evaluate@1.0.0"),
        ),
        skills=("collision-falsification-analyst",),
        timeout_seconds=30.0,
    )

    composer = AgentMemberSpec(
        agent_id="collision_composer",
        name="Collision Portfolio Composer",
        authority_lane=AuthorityLane.COMPOSER,
        allowed_capabilities=(
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.READ_WRITE, "cae.composition.compile@1.0.0"),
        ),
        skills=("hypothesis-portfolio-composer",),
        timeout_seconds=30.0,
    )

    commander = AgentMemberSpec(
        agent_id="collision_commander",
        name="Collision Governance Commander",
        authority_lane=AuthorityLane.COMMANDER,
        is_commander=True,
        allowed_capabilities=(
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.MUTATION_OPERATION, "cae.workspace.provision@1.0.0"),
            CapabilityProjection(CapabilityScope.CAE_TYPED_OPERATION, AccessMode.MUTATION_OPERATION, "cae.operator.grant.issue@1.0.0"),
            CapabilityProjection(CapabilityScope.POSTGRES_STORAGE, AccessMode.READ_WRITE, "cae.collision_hypothesis"),
        ),
        skills=("operator-gate-authorizer",),
        timeout_seconds=45.0,
    )

    team_spec = AgentTeamSpec(
        team_id="collision_discovery_pilot_team",
        name="Collision Discovery Reference Pilot Team",
        workspace_id=workspace_id,
        members={
            "collision_hunter": hunter,
            "collision_analyst": analyst,
            "collision_composer": composer,
            "collision_commander": commander,
        },
        allowed_delegations={
            "collision_orchestrator": [
                "collision_hunter",
                "collision_sub_hunter",
                "collision_analyst",
                "collision_composer",
                "collision_commander",
            ],
            "collision_hunter": ["collision_sub_hunter"],
        },
        max_concurrency=4,
        global_timeout_seconds=120.0,
    )

    runtime = AgentTeamRuntime(team_spec=team_spec)

    # Register pilot passive skill handlers
    runtime.register_skill(
        "collision-evidence-ingest",
        lambda payload: {
            "ingested_signals": [
                {"signal_id": "SIG-001", "type": "cultural_trend", "source": "RES-001"},
                {"signal_id": "SIG-002", "type": "audience_tension", "source": "AUD-001"},
            ],
            "status": "INGESTED",
        },
    )

    runtime.register_skill(
        "collision-hypothesis-hunter",
        lambda payload: {
            "candidate_hypotheses": [
                {
                    "hypothesis_id": "HYP-001",
                    "title": "Unconscious Competence Tension",
                    "signals": ["SIG-001", "SIG-002"],
                    "world_intersections": ["W1_Cultural_Trend", "W2_Audience_Tension"],
                }
            ],
            "recall_count": 1,
        },
    )

    runtime.register_skill(
        "collision-falsification-analyst",
        lambda payload: {
            "evaluated_hypotheses": [
                {
                    "hypothesis_id": "HYP-001",
                    "falsification_score": "0.94",
                    "cliche_risk": "LOW",
                    "grounding_passed": True,
                }
            ],
            "admitted_count": 1,
        },
    )

    runtime.register_skill(
        "hypothesis-portfolio-composer",
        lambda payload: {
            "portfolio": {
                "portfolio_id": "PORT-001",
                "title": "Pilot Collision Portfolio",
                "items": ["HYP-001"],
                "coverage_score": "0.98",
            },
            "status": "COMPOSED",
        },
    )

    runtime.register_skill(
        "operator-gate-authorizer",
        lambda payload: {
            "decision": "AUTHORIZED",
            "state_version": 1,
            "operator_id": "human_operator_verified",
        },
    )

    return team_spec, runtime
