"""Standalone Agent Session Runtime for CAE.

Governed by:
- Phase 6 Mandate M56 (01_AGENT_EXECUTION/M56_standalone_agent_session_runtime.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Enforces:
1. Independently Addressable Agent Session Envelope:
   Enables Agent execution outside Programs for review, debugging, debate, planning,
   and incident investigation while preserving governance, scope, and evidence models.
2. Uniform Agent Definition Contract:
   The same registered AgentDefinition works in both Program binding (M53) and Standalone Sessions.
3. Explicit Authority and Scope Boundaries:
   Every session has an immutable, cryptographically hashed scope (tools, evidence, read-only constraints,
   invocation budget) preventing ambient access or privilege escalation.
4. Context Isolation and Anti-Leak Invariance:
   Sessions compile isolated context capsules; cross-session or stale Program context reuse is detected and blocked.
5. Checked Lifecycle Transitions and StateM Alignment:
   State transitions (CREATED -> AUTHORIZED -> ACTIVE -> PAUSED -> COMPLETED / FAILED) follow checked transfer semantics.
6. Reversible, Non-Mutating Execution:
   Standalone sessions cannot write to canonical state without explicit governed operation authorization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.agent_invocation import (
    AgentInvocation,
    AgentInvocationCompiler,
    AgentInvocationReceipt,
    AgentInvocationRuntime,
)
from ca_runtime.agent_registry import (
    AgentDefinition,
    AgentLifecycleState,
    AgentLifecycleViolationError,
    AgentRegistry,
    AgentResolver,
    PRODUCTION_RESOLVABLE_STATES,
    StandaloneAgentSession,
    get_agent_registry,
    get_agent_resolver,
)
from ca_runtime.agent_result_gates import (
    AgentResultGateEngine,
    AgentResultGateEvaluation,
    TypedAgentResult,
)
from ca_runtime.bounded_repair import (
    BoundedRepairRuntimeEngine,
    BoundedRepairSession,
    RepairAttemptRecord,
)
from ca_runtime.context_capsule import (
    AccessMode,
    CapabilityProjection,
    CapabilityScope,
    CompiledAgentPackage,
    HierarchicalContextResolver,
    JITContextCapsule,
    JITContextCompiler,
    SkillPackageRef,
)
from ca_runtime.pi_adapter import AuthorityLane

logger = logging.getLogger("ca_runtime.standalone_session")


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class AgentSessionError(RuntimeError):
    """Base exception for standalone agent session operations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "AGENT_SESSION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class SessionNotFoundError(AgentSessionError):
    """Raised when a requested session_id is not found."""

    def __init__(self, session_id: str):
        super().__init__(
            f"Session '{session_id}' not found",
            reason_code="SESSION_NOT_FOUND",
            details={"session_id": session_id},
        )


class SessionAuthorizationRequiredError(AgentSessionError):
    """Raised when an un-authorized session attempts governed invocation."""

    def __init__(self, session_id: str, current_state: str):
        super().__init__(
            f"SESSION_AUTHORIZATION_REQUIRED: Session '{session_id}' is in '{current_state}' state. "
            f"Operator authorization is required before invocation.",
            reason_code="SESSION_AUTHORIZATION_REQUIRED",
            details={"session_id": session_id, "current_state": current_state},
        )


class SessionScopeViolationError(AgentSessionError):
    """Raised when an execution violates declared session scope boundaries."""

    def __init__(self, session_id: str, reason: str, details: Optional[Dict[str, Any]] = None):
        d = details or {}
        d["session_id"] = session_id
        super().__init__(
            f"SESSION_SCOPE_VIOLATION: Session '{session_id}' scope boundary exceeded: {reason}",
            reason_code="SESSION_SCOPE_VIOLATION",
            details=d,
        )


class SessionContextLeakError(AgentSessionError):
    """Raised when cross-session context contamination or stale Program context is detected."""

    def __init__(self, session_id: str, reason: str, details: Optional[Dict[str, Any]] = None):
        d = details or {}
        d["session_id"] = session_id
        super().__init__(
            f"SESSION_CONTEXT_LEAK_DETECTED: Session '{session_id}' context isolation failed: {reason}",
            reason_code="SESSION_CONTEXT_LEAK_DETECTED",
            details=d,
        )


class SessionToolEscalationError(AgentSessionError):
    """Raised when a session requests tools broader than authorized by the agent package."""

    def __init__(self, agent_id: str, requested_tool: str, allowed_tools: Sequence[str]):
        super().__init__(
            f"SESSION_TOOL_ESCALATION: Agent '{agent_id}' requested tool '{requested_tool}' which "
            f"exceeds declared agent package capabilities: {list(allowed_tools)}",
            reason_code="SESSION_TOOL_ESCALATION",
            details={
                "agent_id": agent_id,
                "requested_tool": requested_tool,
                "allowed_tools": list(allowed_tools),
            },
        )


class SessionCanonicalWriteBlockedError(AgentSessionError):
    """Raised when a read-only standalone session attempts to mutate canonical state."""

    def __init__(self, session_id: str, attempted_operation: str):
        super().__init__(
            f"CANONICAL_WRITE_BLOCKED: Standalone session '{session_id}' is read-only and cannot "
            f"perform canonical state mutation '{attempted_operation}'",
            reason_code="CANONICAL_WRITE_BLOCKED",
            details={"session_id": session_id, "attempted_operation": attempted_operation},
        )


class SessionLifecycleViolationError(AgentSessionError):
    """Raised when an invalid session lifecycle transition is attempted."""

    def __init__(self, session_id: str, from_state: str, attempted_action: str):
        super().__init__(
            f"LIFECYCLE_VIOLATION: Cannot perform '{attempted_action}' on session '{session_id}' in state '{from_state}'",
            reason_code="SESSION_LIFECYCLE_VIOLATION",
            details={"session_id": session_id, "from_state": from_state, "attempted_action": attempted_action},
        )


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SessionPurpose(str, Enum):
    """Purpose classification for Standalone Agent Sessions."""
    REVIEW = "REVIEW"
    DEBUG = "DEBUG"
    DEBATE = "DEBATE"
    PLANNING = "PLANNING"
    INCIDENT_INVESTIGATION = "INCIDENT_INVESTIGATION"


class SessionLifecycleState(str, Enum):
    """Governed lifecycle states for Standalone Agent Sessions."""
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Domain Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AgentSessionScope:
    """Immutable, hash-addressed scope boundary governing what an Agent can access in a session."""
    workspace_id: UUID
    allowed_evidence_ids: Tuple[str, ...] = field(default_factory=tuple)
    allowed_tools: Tuple[str, ...] = field(default_factory=tuple)
    forbidden_actions: Tuple[str, ...] = field(default_factory=tuple)
    read_only: bool = True
    max_invocations: int = 10
    scope_sha256: str = field(default="")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "workspace_id": str(self.workspace_id),
            "allowed_evidence_ids": list(sorted(self.allowed_evidence_ids)),
            "allowed_tools": list(sorted(self.allowed_tools)),
            "forbidden_actions": list(sorted(self.forbidden_actions)),
            "read_only": self.read_only,
            "max_invocations": int(self.max_invocations),
        }

    def compute_sha256(self) -> str:
        return canonical_sha256(canonical_json_text(self.canonical_dict()))


@dataclass(frozen=True, slots=True)
class AgentSessionRecord:
    """The authoritative record of an independently addressable Standalone Agent Session."""
    session_id: str
    workspace_id: UUID
    agent_id: str
    agent_version: str
    authority_lane: AuthorityLane
    purpose: SessionPurpose
    scope: AgentSessionScope
    lifecycle_state: SessionLifecycleState
    operator_authorization_id: Optional[str] = None
    context_sha256_at_creation: str = ""
    invocation_history: Tuple[str, ...] = field(default_factory=tuple)
    repair_sessions: Tuple[str, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=utc_now_rfc3339)
    updated_at: str = field(default_factory=utc_now_rfc3339)
    session_sha256: str = field(default="")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "workspace_id": str(self.workspace_id),
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "authority_lane": self.authority_lane.value,
            "purpose": self.purpose.value,
            "scope_sha256": self.scope.scope_sha256 or self.scope.compute_sha256(),
            "lifecycle_state": self.lifecycle_state.value,
            "operator_authorization_id": self.operator_authorization_id,
            "context_sha256_at_creation": self.context_sha256_at_creation,
            "invocation_history": list(self.invocation_history),
            "repair_sessions": list(self.repair_sessions),
            "created_at": self.created_at,
        }

    def compute_sha256(self) -> str:
        return canonical_sha256(canonical_json_text(self.canonical_dict()))


@dataclass(frozen=True, slots=True)
class AgentSessionReceipt:
    """Immutable receipt proving governed standalone session execution and terminal outcome."""
    receipt_id: str
    session_id: str
    agent_id: str
    workspace_id: UUID
    purpose: str
    lifecycle_state: str
    invocation_count: int
    repair_count: int
    scope_sha256: str
    operator_authorization_id: Optional[str]
    completed_at: str
    receipt_sha256: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "workspace_id": str(self.workspace_id),
            "purpose": self.purpose,
            "lifecycle_state": self.lifecycle_state,
            "invocation_count": int(self.invocation_count),
            "repair_count": int(self.repair_count),
            "scope_sha256": self.scope_sha256,
            "operator_authorization_id": self.operator_authorization_id,
            "completed_at": self.completed_at,
        }


# ---------------------------------------------------------------------------
# Standalone Agent Session Runtime Engine
# ---------------------------------------------------------------------------

class AgentSessionRuntime:
    """Authoritative runtime coordinating standalone agent sessions, scope boundaries, and execution."""

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        resolver: Optional[AgentResolver] = None,
    ) -> None:
        self.registry = registry or get_agent_registry()
        self.resolver = resolver or (AgentResolver(self.registry) if self.registry else get_agent_resolver())
        self._sessions: Dict[str, AgentSessionRecord] = {}
        self._session_capsules: Dict[str, JITContextCapsule] = {}
        self._receipts: Dict[str, AgentSessionReceipt] = {}

    def start(
        self,
        *,
        agent_id: str,
        purpose: SessionPurpose,
        workspace_id: UUID,
        scope: Optional[AgentSessionScope] = None,
        agent_version: Optional[str] = None,
        operator_id: Optional[str] = None,
        auto_authorize: bool = False,
    ) -> AgentSessionRecord:
        """Start a new Standalone Agent Session.
        
        Enforces:
        1. Agent must be registered in APPROVED or ACTIVE state.
        2. Scope tool boundaries cannot exceed declared agent package capabilities.
        3. Initial state is CREATED (or AUTHORIZED if operator_id provided with auto_authorize).
        """
        agent = self.resolver.resolve(
            agent_id=agent_id,
            version=agent_version,
            min_lifecycle=AgentLifecycleState.APPROVED,
        )

        # Build and validate scope
        if scope is None:
            scope = AgentSessionScope(
                workspace_id=workspace_id,
                allowed_tools=tuple(sorted(agent.tools)),
                read_only=True,
                max_invocations=10,
            )

        # Enforce scope tool boundaries: cannot escalate tools beyond agent package
        allowed_package_tools: Set[str] = set(agent.tools)
        for skill in agent.skills:
            # skills may reference tools
            allowed_package_tools.add(f"skill:{skill.name}")
        for cap in agent.capabilities:
            allowed_package_tools.add(cap.target)

        for req_tool in scope.allowed_tools:
            if req_tool in scope.forbidden_actions:
                raise SessionToolEscalationError(agent_id, req_tool, list(allowed_package_tools))
            if req_tool not in allowed_package_tools and not req_tool.startswith("tool:default-"):
                raise SessionToolEscalationError(agent_id, req_tool, list(allowed_package_tools))

        computed_scope_sha = scope.compute_sha256()
        if not scope.scope_sha256 or scope.scope_sha256 != computed_scope_sha:
            scope = AgentSessionScope(
                workspace_id=scope.workspace_id,
                allowed_evidence_ids=scope.allowed_evidence_ids,
                allowed_tools=scope.allowed_tools,
                forbidden_actions=scope.forbidden_actions,
                read_only=scope.read_only,
                max_invocations=scope.max_invocations,
                scope_sha256=computed_scope_sha,
            )

        session_id = f"sess_standalone_{agent.agent_id}_{uuid4().hex[:12]}"
        created_at = utc_now_rfc3339()

        # Compile initial isolated context capsule for session
        capsule = JITContextCompiler.assemble(
            workspace_id=workspace_id,
            lane=agent.authority_lane,
            actor_id=operator_id or f"actor_session_{session_id}",
            program_id=f"standalone_{purpose.value.lower()}",
            harness_id=f"standalone_session_{session_id}",
            agent_id=agent.agent_id,
            model_id=agent.model_policy.preferred_model,
            total_token_budget=agent.model_policy.token_budget,
            agent_instructions=(
                agent.prompt_reference.instructions_ref or "instructions.md",
                f"Execute standalone session reasoning for purpose '{purpose.value}'.",
            ),
            artifacts=[
                (f"ev_{ev_id}", f"evidence/{ev_id}", f"Allowed evidence reference: {ev_id}")
                for ev_id in scope.allowed_evidence_ids
            ],
            capabilities=[
                CapabilityProjection(
                    capability_id=f"cap:{cap.scope.value}:{cap.target}",
                    owner_product="cae",
                    scope=cap.scope,
                    mode=cap.mode,
                    workspace_bound=True,
                    approval_required=cap.approval_required,
                    sandbox_required=False,
                    audit_mode="FULL",
                    bound_tools=tuple(agent.tools),
                    mcp_servers=(),
                )
                for cap in agent.capabilities
            ],
        )
        self._session_capsules[session_id] = capsule

        initial_state = SessionLifecycleState.CREATED
        auth_id = None
        if auto_authorize and operator_id:
            initial_state = SessionLifecycleState.AUTHORIZED
            auth_id = operator_id

        partial_record = {
            "session_id": session_id,
            "workspace_id": str(workspace_id),
            "agent_id": agent.agent_id,
            "agent_version": agent.version,
            "authority_lane": agent.authority_lane.value,
            "purpose": purpose.value,
            "scope_sha256": scope.scope_sha256,
            "lifecycle_state": initial_state.value,
            "operator_authorization_id": auth_id,
            "context_sha256_at_creation": capsule.capsule_sha256,
            "invocation_history": [],
            "repair_sessions": [],
            "created_at": created_at,
        }
        session_sha = canonical_sha256(canonical_json_text(partial_record))

        record = AgentSessionRecord(
            session_id=session_id,
            workspace_id=workspace_id,
            agent_id=agent.agent_id,
            agent_version=agent.version,
            authority_lane=agent.authority_lane,
            purpose=purpose,
            scope=scope,
            lifecycle_state=initial_state,
            operator_authorization_id=auth_id,
            context_sha256_at_creation=capsule.capsule_sha256,
            invocation_history=(),
            repair_sessions=(),
            created_at=created_at,
            updated_at=created_at,
            session_sha256=session_sha,
        )

        self._sessions[session_id] = record
        logger.info(f"Started standalone agent session: {session_id} [{agent.agent_id} | {purpose.value}]")
        return record

    def authorize(
        self,
        session_id: str,
        *,
        operator_id: str,
    ) -> AgentSessionRecord:
        """Authorize a CREATED session for execution."""
        session = self.get_session(session_id)
        if session.lifecycle_state not in (SessionLifecycleState.CREATED, SessionLifecycleState.PAUSED):
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "authorize")

        updated_at = utc_now_rfc3339()
        updated_record = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.AUTHORIZED,
            operator_authorization_id=operator_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=session.invocation_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=updated_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_record
        logger.info(f"Authorized session {session_id} by operator {operator_id}")
        return updated_record

    def invoke(
        self,
        session_id: str,
        task_prompt: str,
        *,
        capsule: Optional[JITContextCapsule] = None,
        inference_fn: Optional[Callable[[AgentInvocation], Dict[str, Any]]] = None,
        model_reasoning_engine: Optional[Any] = None,
        requested_tools: Optional[Sequence[str]] = None,
        is_canonical_mutation: bool = False,
    ) -> AgentInvocationReceipt:
        """Execute a governed invocation within the session envelope.
        
        Enforces:
        1. Session must be in AUTHORIZED or ACTIVE state.
        2. Session invocation budget (max_invocations) is not exceeded.
        3. Context isolation: verifies capsule was compiled for this session and workspace.
        4. Read-only scope blocks canonical mutations.
        5. Emits verifiable AgentInvocationReceipt and updates session invocation history.
        """
        session = self.get_session(session_id)

        # 1. State Verification
        if session.lifecycle_state == SessionLifecycleState.CREATED:
            raise SessionAuthorizationRequiredError(session_id, session.lifecycle_state.value)
        if session.lifecycle_state in (SessionLifecycleState.PAUSED, SessionLifecycleState.COMPLETED, SessionLifecycleState.FAILED):
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "invoke")

        # 2. Scope Budget Check
        if len(session.invocation_history) >= session.scope.max_invocations:
            raise SessionScopeViolationError(
                session_id,
                f"Maximum invocations ({session.scope.max_invocations}) exceeded for this session",
                details={"invocations_count": len(session.invocation_history), "max": session.scope.max_invocations},
            )

        # 3. Read-Only Mutation Gate
        if is_canonical_mutation and session.scope.read_only:
            raise SessionCanonicalWriteBlockedError(session_id, "state_mutation_attempt")

        # 4. Context Isolation and Anti-Leak Verification
        effective_capsule = capsule or self._session_capsules.get(session_id)
        if effective_capsule is None:
            raise SessionContextLeakError(session_id, "No context capsule available for session")

        if effective_capsule.workspace_id != session.workspace_id:
            raise SessionContextLeakError(
                session_id,
                f"Context capsule belongs to workspace {effective_capsule.workspace_id}, but session is in {session.workspace_id}",
                details={"capsule_workspace": str(effective_capsule.workspace_id), "session_workspace": str(session.workspace_id)},
            )

        # Verify that stale Program context or cross-session capsule is not leaked
        expected_harness = f"standalone_session_{session_id}"
        if effective_capsule.harness_id != expected_harness:
            raise SessionContextLeakError(
                session_id,
                f"Cross-session/stale context leak: capsule was compiled for harness '{effective_capsule.harness_id}' rather than '{expected_harness}'",
                details={"capsule_harness_id": effective_capsule.harness_id, "expected_harness": expected_harness},
            )

        # 5. Retrieve Agent Definition
        agent = self.registry.get(session.agent_id, session.agent_version)

        # 6. Verify requested tools against session scope
        tools_to_use = requested_tools if requested_tools is not None else session.scope.allowed_tools
        for t in tools_to_use:
            if t not in session.scope.allowed_tools:
                raise SessionScopeViolationError(
                    session_id,
                    f"Tool '{t}' is outside session scope allowed tools",
                    details={"tool": t, "allowed_tools": list(session.scope.allowed_tools)},
                )

        # 7. Compile AgentInvocation
        system_prompt = (
            f"You are CAE Agent '{session.agent_id}' executing in Standalone Session '{session_id}' "
            f"for purpose '{session.purpose.value}'. Authority Lane: '{session.authority_lane.value}'."
        )

        invocation = AgentInvocationCompiler.compile(
            agent=agent,
            capsule=effective_capsule,
            workspace_id=session.workspace_id,
            run_id=session_id,
            state_id=session.purpose.value,
            model_id=agent.model_policy.preferred_model,
            requested_tools=tools_to_use,
            system_prompt=system_prompt,
            output_contract=agent.output_contract,
        )

        # 8. Execute via AgentInvocationRuntime
        receipt = AgentInvocationRuntime.execute(
            invocation=invocation,
            inference_fn=inference_fn,
            model_reasoning_engine=model_reasoning_engine,
        )

        # 9. Update Session state to ACTIVE and record invocation
        updated_inv_history = tuple(list(session.invocation_history) + [receipt.receipt_id])
        updated_at = utc_now_rfc3339()

        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.ACTIVE,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=updated_inv_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=updated_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        return receipt

    def execute_with_repair(
        self,
        session_id: str,
        task_prompt: str,
        *,
        inference_fn: Callable[[AgentInvocation, Optional[RepairAttemptRecord]], str],
        gate_evaluator: Callable[[str, AgentInvocation], Tuple[TypedAgentResult, AgentResultGateEvaluation]],
        max_retries: int = 2,
    ) -> Tuple[TypedAgentResult, BoundedRepairSession]:
        """Execute within the session using BoundedRepairRuntimeEngine for same-session retry."""
        session = self.get_session(session_id)
        if session.lifecycle_state == SessionLifecycleState.CREATED:
            raise SessionAuthorizationRequiredError(session_id, session.lifecycle_state.value)
        if session.lifecycle_state in (SessionLifecycleState.PAUSED, SessionLifecycleState.COMPLETED, SessionLifecycleState.FAILED):
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "execute_with_repair")

        agent = self.registry.get(session.agent_id, session.agent_version)
        effective_capsule = self._session_capsules.get(session_id)
        if effective_capsule is None:
            raise SessionContextLeakError(session_id, "No context capsule available for session")

        system_prompt = (
            f"You are CAE Agent '{session.agent_id}' executing in Standalone Session '{session_id}' "
            f"for purpose '{session.purpose.value}'. Authority Lane: '{session.authority_lane.value}'."
        )

        invocation = AgentInvocationCompiler.compile(
            agent=agent,
            capsule=effective_capsule,
            workspace_id=session.workspace_id,
            run_id=session_id,
            state_id=session.purpose.value,
            model_id=agent.model_policy.preferred_model,
            requested_tools=session.scope.allowed_tools,
            system_prompt=system_prompt,
            output_contract=agent.output_contract,
        )

        repair_session = BoundedRepairRuntimeEngine.create_session(
            invocation=invocation,
            max_retries=max_retries,
        )

        typed_result, active_repair_session = BoundedRepairRuntimeEngine.execute_with_repair(
            session=repair_session,
            invocation=invocation,
            inference_fn=inference_fn,
            gate_evaluator=gate_evaluator,
        )

        # Update session with repair record
        updated_repairs = tuple(list(session.repair_sessions) + [active_repair_session.session_id])
        updated_inv_history = tuple(list(session.invocation_history) + [f"repair_inv_{active_repair_session.session_id}"])
        updated_at = utc_now_rfc3339()

        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.ACTIVE,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=updated_inv_history,
            repair_sessions=updated_repairs,
            created_at=session.created_at,
            updated_at=updated_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        return typed_result, active_repair_session

    def pause(
        self,
        session_id: str,
        *,
        operator_id: str,
    ) -> AgentSessionRecord:
        """Pause an active session."""
        session = self.get_session(session_id)
        if session.lifecycle_state != SessionLifecycleState.ACTIVE:
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "pause")

        updated_at = utc_now_rfc3339()
        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.PAUSED,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=session.invocation_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=updated_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        logger.info(f"Paused session {session_id} by operator {operator_id}")
        return updated_session

    def resume(
        self,
        session_id: str,
        *,
        operator_id: str,
    ) -> AgentSessionRecord:
        """Resume a paused session."""
        session = self.get_session(session_id)
        if session.lifecycle_state != SessionLifecycleState.PAUSED:
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "resume")

        updated_at = utc_now_rfc3339()
        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.ACTIVE,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=session.invocation_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=updated_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        logger.info(f"Resumed session {session_id} by operator {operator_id}")
        return updated_session

    def complete(
        self,
        session_id: str,
    ) -> AgentSessionReceipt:
        """Close an active session and emit its cryptographic completion receipt."""
        session = self.get_session(session_id)
        if session.lifecycle_state not in (SessionLifecycleState.ACTIVE, SessionLifecycleState.AUTHORIZED):
            raise SessionLifecycleViolationError(session_id, session.lifecycle_state.value, "complete")

        completed_at = utc_now_rfc3339()
        receipt_id = f"rcpt_sess_{hashlib.sha256(f'{session_id}:{completed_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        partial_receipt = {
            "receipt_id": receipt_id,
            "session_id": session.session_id,
            "agent_id": session.agent_id,
            "workspace_id": str(session.workspace_id),
            "purpose": session.purpose.value,
            "lifecycle_state": SessionLifecycleState.COMPLETED.value,
            "invocation_count": len(session.invocation_history),
            "repair_count": len(session.repair_sessions),
            "scope_sha256": session.scope.scope_sha256,
            "operator_authorization_id": session.operator_authorization_id,
            "completed_at": completed_at,
        }
        receipt_sha = canonical_sha256(canonical_json_text(partial_receipt))

        receipt = AgentSessionReceipt(
            receipt_id=receipt_id,
            session_id=session.session_id,
            agent_id=session.agent_id,
            workspace_id=session.workspace_id,
            purpose=session.purpose.value,
            lifecycle_state=SessionLifecycleState.COMPLETED.value,
            invocation_count=len(session.invocation_history),
            repair_count=len(session.repair_sessions),
            scope_sha256=session.scope.scope_sha256,
            operator_authorization_id=session.operator_authorization_id,
            completed_at=completed_at,
            receipt_sha256=receipt_sha,
        )

        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.COMPLETED,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=session.invocation_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=completed_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        self._receipts[receipt_id] = receipt
        logger.info(f"Completed standalone session {session_id}, emitted receipt {receipt_id}")
        return receipt

    def fail(
        self,
        session_id: str,
        *,
        reason: str,
    ) -> AgentSessionReceipt:
        """Mark a session as FAILED and emit a failure receipt."""
        session = self.get_session(session_id)
        failed_at = utc_now_rfc3339()
        receipt_id = f"rcpt_sess_fail_{hashlib.sha256(f'{session_id}:{failed_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        partial_receipt = {
            "receipt_id": receipt_id,
            "session_id": session.session_id,
            "agent_id": session.agent_id,
            "workspace_id": str(session.workspace_id),
            "purpose": session.purpose.value,
            "lifecycle_state": SessionLifecycleState.FAILED.value,
            "invocation_count": len(session.invocation_history),
            "repair_count": len(session.repair_sessions),
            "scope_sha256": session.scope.scope_sha256,
            "operator_authorization_id": session.operator_authorization_id,
            "completed_at": failed_at,
        }
        receipt_sha = canonical_sha256(canonical_json_text(partial_receipt))

        receipt = AgentSessionReceipt(
            receipt_id=receipt_id,
            session_id=session.session_id,
            agent_id=session.agent_id,
            workspace_id=session.workspace_id,
            purpose=session.purpose.value,
            lifecycle_state=SessionLifecycleState.FAILED.value,
            invocation_count=len(session.invocation_history),
            repair_count=len(session.repair_sessions),
            scope_sha256=session.scope.scope_sha256,
            operator_authorization_id=session.operator_authorization_id,
            completed_at=failed_at,
            receipt_sha256=receipt_sha,
        )

        updated_session = AgentSessionRecord(
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            agent_id=session.agent_id,
            agent_version=session.agent_version,
            authority_lane=session.authority_lane,
            purpose=session.purpose,
            scope=session.scope,
            lifecycle_state=SessionLifecycleState.FAILED,
            operator_authorization_id=session.operator_authorization_id,
            context_sha256_at_creation=session.context_sha256_at_creation,
            invocation_history=session.invocation_history,
            repair_sessions=session.repair_sessions,
            created_at=session.created_at,
            updated_at=failed_at,
            session_sha256=session.session_sha256,
        )
        self._sessions[session_id] = updated_session
        self._receipts[receipt_id] = receipt
        return receipt

    def get_session(self, session_id: str) -> AgentSessionRecord:
        """Retrieve a session by ID or raise SessionNotFoundError."""
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions[session_id]

    def list_sessions(
        self,
        *,
        workspace_id: Optional[UUID] = None,
        purpose: Optional[SessionPurpose] = None,
        agent_id: Optional[str] = None,
    ) -> List[AgentSessionRecord]:
        """Query sessions by optional workspace, purpose, or agent_id."""
        results = list(self._sessions.values())
        if workspace_id:
            results = [s for s in results if s.workspace_id == workspace_id]
        if purpose:
            results = [s for s in results if s.purpose == purpose]
        if agent_id:
            results = [s for s in results if s.agent_id == agent_id]
        results.sort(key=lambda s: s.created_at)
        return results

    def inspect(self, session_id: str) -> Dict[str, Any]:
        """Produce full inspectable diagnostic view of a standalone session."""
        session = self.get_session(session_id)
        capsule = self._session_capsules.get(session_id)
        return {
            "session_id": session.session_id,
            "workspace_id": str(session.workspace_id),
            "agent_id": session.agent_id,
            "agent_version": session.agent_version,
            "authority_lane": session.authority_lane.value,
            "purpose": session.purpose.value,
            "lifecycle_state": session.lifecycle_state.value,
            "operator_authorization_id": session.operator_authorization_id,
            "scope": session.scope.canonical_dict(),
            "scope_sha256": session.scope.scope_sha256,
            "invocations_count": len(session.invocation_history),
            "repairs_count": len(session.repair_sessions),
            "context_capsule_sha256": capsule.capsule_sha256 if capsule else None,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "session_sha256": session.session_sha256,
        }
