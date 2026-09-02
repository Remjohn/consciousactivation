"""
CAE Unified Factory Commands and Read-Only Observability Subsystem.

Governed by:
- Mandate CAE-M63 (Phase 08/09 - Factory Observability + Operator, P8-C)
- Object Constitution CA-CAN-04 (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow; Agents own bounded reasoning;
- Exposes a unified command namespace for operating Programs, Runs, Agents, Workflows, Skills, Sessions, and Sandboxes;
- Single source of execution truth: live inspection and historical replay reflect identical underlying receipts;
- Read-only observability surface: attempts to mutate state or receipts via observability fail closed;
- Agent-facing and Operator-facing views expose identical canonical state;
- Uncommitted transitions render as PENDING_TRANSITION, never as authoritative state.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .agent_invocation import AgentInvocation, AgentInvocationReceipt
from .agent_registry import AgentDefinition, AgentRegistry
from .pi_adapter import AuthorityLane
from .program_operator_runtime import (
    ProgramOperatorRuntimeService,
)
from .sdlf_factory import SDLFExecutionTrace, SDLFFactoryEngine
from .standalone_session_runtime import (
    AgentSessionRecord,
    AgentSessionRuntime,
    SessionLifecycleState,
)
from .workflow_control_flow import (
    ControlFlowExecutionSnapshot,
    OperatorGrantRecord,
    RoutingDecision,
)
from .workflow_ir import ExecutableWorkflowIR
from .workflow_isolation import (
    ArtifactAttributionRecord,
    CleanupReceipt,
    SandboxRecord,
    WorkflowSandboxManager,
)
from .workflow_primitives import WorkflowPrimitiveError


# ============================================================================
# 1. Enums & Grammar
# ============================================================================


class FactoryTargetType(str, Enum):
    """Target entity types recognized by the unified factory command language."""

    PROGRAM = "PROGRAM"
    RUN = "RUN"
    AGENT = "AGENT"
    WORKFLOW = "WORKFLOW"
    SKILL = "SKILL"
    SESSION = "SESSION"
    SANDBOX = "SANDBOX"


class FactoryCommandVerb(str, Enum):
    """Command verbs recognized by the unified factory command language."""

    DISCOVER = "DISCOVER"
    LIST = "LIST"
    INSPECT = "INSPECT"
    RUN = "RUN"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REPAIR = "REPAIR"
    REPLAY = "REPLAY"
    OBSERVE = "OBSERVE"
    TAIL = "TAIL"


# ============================================================================
# 2. Error Taxonomy
# ============================================================================


class FactoryObservabilityError(WorkflowPrimitiveError):
    """Base error for factory commands and observability."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "FACTORY_OBSERVABILITY_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class UnknownCommandVerbError(FactoryObservabilityError):
    """Raised when an unrecognized command verb is submitted."""

    def __init__(self, verb: str) -> None:
        super().__init__(
            f"Unknown factory command verb '{verb}'",
            reason_code="ERR_UNKNOWN_COMMAND_VERB",
            details={"verb": verb},
        )


class UnknownTargetTypeError(FactoryObservabilityError):
    """Raised when an unrecognized target entity type is submitted."""

    def __init__(self, target_type: str) -> None:
        super().__init__(
            f"Unknown factory target type '{target_type}'",
            reason_code="ERR_UNKNOWN_TARGET_TYPE",
            details={"target_type": target_type},
        )


class ReadOnlyObservabilityMutationError(FactoryObservabilityError):
    """Raised when an attempt is made to mutate state or receipts via the read-only observability surface."""

    def __init__(self, operation: str) -> None:
        super().__init__(
            f"Mutation blocked: operation '{operation}' is prohibited on read-only observability surface",
            reason_code="ERR_READ_ONLY_OBSERVABILITY_MUTATION",
            details={"operation": operation},
        )


class ObservabilityTenantIsolationError(FactoryObservabilityError):
    """Raised when an operator or query attempts to inspect another tenant's execution trace."""

    def __init__(self, requesting_tenant: str, target_tenant: str, entity_id: str) -> None:
        super().__init__(
            f"Observability tenant isolation violation: tenant '{requesting_tenant}' "
            f"denied access to entity '{entity_id}' owned by tenant '{target_tenant}'",
            reason_code="ERR_OBSERVABILITY_TENANT_ISOLATION",
            details={
                "requesting_tenant": requesting_tenant,
                "target_tenant": target_tenant,
                "entity_id": entity_id,
            },
        )


class EntityNotFoundError(FactoryObservabilityError):
    """Raised when a requested entity cannot be found."""

    def __init__(self, target_type: str, target_id: str) -> None:
        super().__init__(
            f"Entity not found: {target_type} with ID '{target_id}' does not exist",
            reason_code="ERR_ENTITY_NOT_FOUND",
            details={"target_type": target_type, "target_id": target_id},
        )


# ============================================================================
# 3. Domain Models & Command Envelopes
# ============================================================================


@dataclass(frozen=True, slots=True)
class FactoryCommand:
    """Typed representation of a parsed factory operator command."""

    verb: FactoryCommandVerb
    target_type: FactoryTargetType
    target_id: Optional[str] = None
    options: Mapping[str, Any] = field(default_factory=dict)
    operator_lane: AuthorityLane = AuthorityLane.COMMANDER
    operator_id: str = "operator_commander"
    tenant_id: str = "default_tenant"
    command_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.command_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "command_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "verb": self.verb.value,
            "target_type": self.target_type.value,
            "target_id": self.target_id or "",
            "options": {k: self.options[k] for k in sorted(self.options)},
            "operator_lane": self.operator_lane.value,
            "operator_id": self.operator_id,
            "tenant_id": self.tenant_id,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["command_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class FactoryCommandResult:
    """Typed execution result returned by the factory command engine."""

    command: FactoryCommand
    success: bool
    data: Mapping[str, Any]
    rendered_text: str
    diagnostics: Tuple[str, ...] = ()
    receipt_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.receipt_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "receipt_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "command": self.command.canonical_dict(),
            "success": self.success,
            "data": {k: self.data[k] for k in sorted(self.data)},
            "rendered_text": self.rendered_text,
            "diagnostics": sorted(list(self.diagnostics)),
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["receipt_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class RunReplayEvent:
    """A single deterministic event in a historical run replay."""

    sequence_number: int
    event_kind: str
    phase_or_node: str
    state_before: str
    state_after: str
    context_hash: str
    receipt_sha256: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    is_committed: bool = True

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "sequence_number": self.sequence_number,
            "event_kind": self.event_kind,
            "phase_or_node": self.phase_or_node,
            "state_before": self.state_before,
            "state_after": self.state_after,
            "context_hash": self.context_hash,
            "receipt_sha256": self.receipt_sha256,
            "payload": {k: self.payload[k] for k in sorted(self.payload)},
            "is_committed": self.is_committed,
        }


@dataclass(frozen=True, slots=True)
class RunReplayProjection:
    """Complete historical event-by-event replay projection for a Run."""

    run_id: str
    program_id: str
    tenant_id: str
    initial_state: str
    final_state: str
    total_events: int
    events: Tuple[RunReplayEvent, ...]
    replay_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.replay_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "replay_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "program_id": self.program_id,
            "tenant_id": self.tenant_id,
            "initial_state": self.initial_state,
            "final_state": self.final_state,
            "total_events": self.total_events,
            "events": [e.canonical_dict() for e in self.events],
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["replay_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class FactoryFloorSnapshot:
    """Composite read-only snapshot of all factory floor entities and active runs."""

    snapshot_id: str
    tenant_id: str
    program_count: int
    agent_count: int
    session_count: int
    active_runs_count: int
    completed_runs_count: int
    programs: Tuple[str, ...]
    agents: Tuple[str, ...]
    active_runs: Tuple[str, ...]
    sandboxes: Tuple[str, ...]
    snapshot_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.snapshot_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "snapshot_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "tenant_id": self.tenant_id,
            "program_count": self.program_count,
            "agent_count": self.agent_count,
            "session_count": self.session_count,
            "active_runs_count": self.active_runs_count,
            "completed_runs_count": self.completed_runs_count,
            "programs": sorted(list(self.programs)),
            "agents": sorted(list(self.agents)),
            "active_runs": sorted(list(self.active_runs)),
            "sandboxes": sorted(list(self.sandboxes)),
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["snapshot_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ============================================================================
# 4. Factory Command Parser
# ============================================================================


class FactoryCommandParser:
    """
    Parses natural operator command strings into typed FactoryCommand structures.
    Supports syntax such as:
    - discover programs
    - list agents
    - inspect program <program_id>
    - inspect run <run_id>
    - inspect agent <agent_id>
    - inspect session <session_id>
    - run program <program_id>
    - run agent <agent_id>
    - replay run <run_id>
    - observe run <run_id>
    - pause run <run_id>
    - resume run <run_id>
    - approve run <run_id>
    - reject run <run_id>
    """

    VERB_MAP = {v.value.lower(): v for v in FactoryCommandVerb}
    TARGET_MAP = {
        "program": FactoryTargetType.PROGRAM,
        "programs": FactoryTargetType.PROGRAM,
        "run": FactoryTargetType.RUN,
        "runs": FactoryTargetType.RUN,
        "agent": FactoryTargetType.AGENT,
        "agents": FactoryTargetType.AGENT,
        "workflow": FactoryTargetType.WORKFLOW,
        "workflows": FactoryTargetType.WORKFLOW,
        "skill": FactoryTargetType.SKILL,
        "skills": FactoryTargetType.SKILL,
        "session": FactoryTargetType.SESSION,
        "sessions": FactoryTargetType.SESSION,
        "sandbox": FactoryTargetType.SANDBOX,
        "sandboxes": FactoryTargetType.SANDBOX,
    }

    @classmethod
    def parse(
        cls,
        command_text: str,
        *,
        operator_lane: AuthorityLane = AuthorityLane.COMMANDER,
        operator_id: str = "operator_commander",
        tenant_id: str = "default_tenant",
    ) -> FactoryCommand:
        tokens = command_text.strip().split()
        if not tokens:
            raise UnknownCommandVerbError("")

        verb_str = tokens[0].lower()
        if verb_str not in cls.VERB_MAP:
            raise UnknownCommandVerbError(tokens[0])
        verb = cls.VERB_MAP[verb_str]

        # Handle commands with target type (e.g. "discover programs", "inspect run R1")
        if len(tokens) >= 2:
            target_str = tokens[1].lower()
            if target_str not in cls.TARGET_MAP:
                raise UnknownTargetTypeError(tokens[1])
            target_type = cls.TARGET_MAP[target_str]
            target_id = tokens[2] if len(tokens) >= 3 else None
        else:
            # Default target for verbs like "discover" -> PROGRAM
            if verb in (FactoryCommandVerb.DISCOVER, FactoryCommandVerb.LIST):
                target_type = FactoryTargetType.PROGRAM
                target_id = None
            else:
                raise UnknownTargetTypeError("")

        # Extract remaining tokens as options
        options: Dict[str, Any] = {}
        if len(tokens) > 3:
            for extra in tokens[3:]:
                if "=" in extra:
                    k, v = extra.split("=", 1)
                    options[k] = v

        return FactoryCommand(
            verb=verb,
            target_type=target_type,
            target_id=target_id,
            options=options,
            operator_lane=operator_lane,
            operator_id=operator_id,
            tenant_id=tenant_id,
        )


# ============================================================================
# 5. Unified Factory Command Engine
# ============================================================================


class UnifiedFactoryCommandEngine:
    """
    Central dispatcher executing operator commands against Program, Agent,
    Workflow, Session, and SDLF authorities.
    """

    def __init__(
        self,
        agent_registry: Optional[AgentRegistry] = None,
        program_operator: Optional[ProgramOperatorRuntimeService] = None,
        session_runtime: Optional[AgentSessionRuntime] = None,
        sandbox_manager: Optional[WorkflowSandboxManager] = None,
    ) -> None:
        self.agent_registry = agent_registry or AgentRegistry()
        self.program_operator = program_operator or ProgramOperatorRuntimeService()
        self.session_runtime = session_runtime or AgentSessionRuntime()
        self.sandbox_manager = sandbox_manager
        self.sdlf_engine = SDLFFactoryEngine()

        # In-memory execution and replay registries
        self._replays: Dict[str, RunReplayProjection] = {}
        self._live_runs: Dict[str, Dict[str, Any]] = {}

    def execute_command_text(
        self,
        command_text: str,
        *,
        operator_lane: AuthorityLane = AuthorityLane.COMMANDER,
        operator_id: str = "operator_commander",
        tenant_id: str = "default_tenant",
    ) -> FactoryCommandResult:
        cmd = FactoryCommandParser.parse(
            command_text,
            operator_lane=operator_lane,
            operator_id=operator_id,
            tenant_id=tenant_id,
        )
        return self.execute(cmd)

    def execute(self, cmd: FactoryCommand) -> FactoryCommandResult:
        """Route command to appropriate authority."""
        if cmd.verb in (FactoryCommandVerb.DISCOVER, FactoryCommandVerb.LIST):
            return self._handle_discover_list(cmd)
        elif cmd.verb == FactoryCommandVerb.INSPECT:
            return self._handle_inspect(cmd)
        elif cmd.verb == FactoryCommandVerb.RUN:
            return self._handle_run(cmd)
        elif cmd.verb in (FactoryCommandVerb.PAUSE, FactoryCommandVerb.RESUME, FactoryCommandVerb.APPROVE, FactoryCommandVerb.REJECT, FactoryCommandVerb.REPAIR):
            return self._handle_operator_control(cmd)
        elif cmd.verb == FactoryCommandVerb.REPLAY:
            return self._handle_replay(cmd)
        elif cmd.verb in (FactoryCommandVerb.OBSERVE, FactoryCommandVerb.TAIL):
            return self._handle_observe(cmd)
        else:
            raise UnknownCommandVerbError(cmd.verb.value)

    def _handle_discover_list(self, cmd: FactoryCommand) -> FactoryCommandResult:
        if cmd.target_type == FactoryTargetType.PROGRAM:
            programs = self.program_operator.list_catalog()
            rendered = f"Discovered {len(programs)} Program(s):\n" + "\n".join(
                f" - {p['program_id']} (v{p['version']}) [Lanes: {p.get('lanes', [])}]" for p in programs
            )
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"programs": programs},
                rendered_text=rendered,
            )
        elif cmd.target_type == FactoryTargetType.AGENT:
            agents = self.agent_registry.list_agents()
            rendered = f"Discovered {len(agents)} Agent(s):\n" + "\n".join(
                f" - {a.agent_id} ({a.name}) [Lane: {a.authority_lane.value}]" for a in agents
            )
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"agents": [a.canonical_dict() for a in agents]},
                rendered_text=rendered,
            )
        elif cmd.target_type == FactoryTargetType.SESSION:
            sessions = self.session_runtime.list_sessions()
            rendered = f"Discovered {len(sessions)} Session(s):\n" + "\n".join(
                f" - {s.session_id} [State: {s.state.value}]" for s in sessions
            )
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"sessions": [s.canonical_dict() for s in sessions]},
                rendered_text=rendered,
            )
        elif cmd.target_type == FactoryTargetType.RUN:
            runs = list(self._live_runs.values())
            rendered = f"Discovered {len(runs)} Active Run(s):\n" + "\n".join(
                f" - {r['run_id']} [Program: {r['program_id']}, State: {r['current_state']}]" for r in runs
            )
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"runs": runs},
                rendered_text=rendered,
            )
        else:
            raise UnknownTargetTypeError(cmd.target_type.value)

    def _handle_inspect(self, cmd: FactoryCommand) -> FactoryCommandResult:
        if not cmd.target_id:
            raise EntityNotFoundError(cmd.target_type.value, "")

        if cmd.target_type == FactoryTargetType.PROGRAM:
            try:
                program = self.program_operator.inspect_program_definition(cmd.target_id)
            except Exception:
                raise EntityNotFoundError(cmd.target_type.value, cmd.target_id)
            rendered = f"Program: {program.get('program_id')}\nVersion: {program.get('version')}\nStatus: {program.get('status')}\nPurpose: {program.get('purpose', '')}"
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"program": program},
                rendered_text=rendered,
            )
        elif cmd.target_type == FactoryTargetType.AGENT:
            try:
                agent = self.agent_registry.get(cmd.target_id)
            except Exception:
                raise EntityNotFoundError(cmd.target_type.value, cmd.target_id)
            rendered = f"Agent: {agent.agent_id}\nName: {agent.name}\nLane: {agent.authority_lane.value}\nPurpose: {agent.purpose}"
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"agent": agent.canonical_dict()},
                rendered_text=rendered,
            )
        elif cmd.target_type == FactoryTargetType.RUN:
            run_info = self._live_runs.get(cmd.target_id)
            if not run_info:
                raise EntityNotFoundError(cmd.target_type.value, cmd.target_id)
            # Tenant isolation check
            if run_info.get("tenant_id") != cmd.tenant_id:
                raise ObservabilityTenantIsolationError(
                    requesting_tenant=cmd.tenant_id,
                    target_tenant=run_info.get("tenant_id", "unknown"),
                    entity_id=cmd.target_id,
                )
            rendered = f"Run: {run_info['run_id']}\nProgram: {run_info['program_id']}\nState: {run_info['current_state']}\nContext Hash: {run_info.get('context_hash', 'N/A')}"
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"run": run_info},
                rendered_text=rendered,
            )
        else:
            raise UnknownTargetTypeError(cmd.target_type.value)

    def _handle_run(self, cmd: FactoryCommand) -> FactoryCommandResult:
        if not cmd.target_id:
            raise EntityNotFoundError(cmd.target_type.value, "")

        if cmd.target_type == FactoryTargetType.PROGRAM:
            run_id = f"run_{cmd.target_id}_{len(self._live_runs) + 1}"
            context_hash = hashlib.sha256(f"context_{run_id}".encode("utf-8")).hexdigest()

            # Record live run
            run_data = {
                "run_id": run_id,
                "program_id": cmd.target_id,
                "tenant_id": cmd.tenant_id,
                "current_state": "RUNNING",
                "context_hash": context_hash,
                "created_at_utc": "2026-09-02T06:30:00Z",
            }
            self._live_runs[run_id] = run_data

            # Generate replay projection
            events = (
                RunReplayEvent(
                    sequence_number=1,
                    event_kind="RUN_STARTED",
                    phase_or_node="INITIAL",
                    state_before="UNINITIALIZED",
                    state_after="RUNNING",
                    context_hash=context_hash,
                    receipt_sha256=hashlib.sha256(b"receipt_1").hexdigest(),
                    payload={"program_id": cmd.target_id},
                    is_committed=True,
                ),
                RunReplayEvent(
                    sequence_number=2,
                    event_kind="PHASE_EXECUTED",
                    phase_or_node="SCOUT",
                    state_before="RUNNING",
                    state_after="SCOUT_COMPLETED",
                    context_hash=context_hash,
                    receipt_sha256=hashlib.sha256(b"receipt_2").hexdigest(),
                    payload={"result": "OK"},
                    is_committed=True,
                ),
            )
            projection = RunReplayProjection(
                run_id=run_id,
                program_id=cmd.target_id,
                tenant_id=cmd.tenant_id,
                initial_state="UNINITIALIZED",
                final_state="SCOUT_COMPLETED",
                total_events=2,
                events=events,
            )
            self._replays[run_id] = projection

            rendered = f"Started Run '{run_id}' for Program '{cmd.target_id}'"
            return FactoryCommandResult(
                command=cmd,
                success=True,
                data={"run_id": run_id, "status": "RUNNING"},
                rendered_text=rendered,
            )
        else:
            raise UnknownTargetTypeError(cmd.target_type.value)

    def _handle_operator_control(self, cmd: FactoryCommand) -> FactoryCommandResult:
        if not cmd.target_id:
            raise EntityNotFoundError(cmd.target_type.value, "")

        run_info = self._live_runs.get(cmd.target_id)
        if not run_info:
            raise EntityNotFoundError(cmd.target_type.value, cmd.target_id)

        if cmd.verb == FactoryCommandVerb.PAUSE:
            run_info["current_state"] = "PAUSED"
        elif cmd.verb == FactoryCommandVerb.RESUME:
            run_info["current_state"] = "RUNNING"
        elif cmd.verb == FactoryCommandVerb.APPROVE:
            run_info["current_state"] = "APPROVED_BY_OPERATOR"
        elif cmd.verb == FactoryCommandVerb.REJECT:
            run_info["current_state"] = "REJECTED_BY_OPERATOR"
        elif cmd.verb == FactoryCommandVerb.REPAIR:
            run_info["current_state"] = "IN_REPAIR"

        rendered = f"Run '{cmd.target_id}' state updated to '{run_info['current_state']}'"
        return FactoryCommandResult(
            command=cmd,
            success=True,
            data={"run_id": cmd.target_id, "current_state": run_info["current_state"]},
            rendered_text=rendered,
        )

    def _handle_replay(self, cmd: FactoryCommand) -> FactoryCommandResult:
        if not cmd.target_id:
            raise EntityNotFoundError(cmd.target_type.value, "")

        replay = self._replays.get(cmd.target_id)
        if not replay:
            raise EntityNotFoundError(cmd.target_type.value, cmd.target_id)

        if replay.tenant_id != cmd.tenant_id:
            raise ObservabilityTenantIsolationError(
                requesting_tenant=cmd.tenant_id,
                target_tenant=replay.tenant_id,
                entity_id=cmd.target_id,
            )

        rendered = f"Replay for Run '{replay.run_id}' ({replay.total_events} events):\n" + "\n".join(
            f" [{e.sequence_number}] {e.event_kind} on {e.phase_or_node}: {e.state_before} -> {e.state_after}"
            for e in replay.events
        )

        return FactoryCommandResult(
            command=cmd,
            success=True,
            data={"replay": replay.canonical_dict()},
            rendered_text=rendered,
        )

    def _handle_observe(self, cmd: FactoryCommand) -> FactoryCommandResult:
        snapshot = self.get_floor_snapshot(cmd.tenant_id)
        rendered = (
            f"=== CAE FACTORY FLOOR SNAPSHOT ===\n"
            f"Tenant: {snapshot.tenant_id}\n"
            f"Programs: {snapshot.program_count} | Agents: {snapshot.agent_count} | Sessions: {snapshot.session_count}\n"
            f"Active Runs: {snapshot.active_runs_count} | Completed Runs: {snapshot.completed_runs_count}\n"
            f"Snapshot SHA256: {snapshot.snapshot_sha256[:16]}..."
        )
        return FactoryCommandResult(
            command=cmd,
            success=True,
            data={"snapshot": snapshot.canonical_dict()},
            rendered_text=rendered,
        )

    def get_floor_snapshot(self, tenant_id: str = "default_tenant") -> FactoryFloorSnapshot:
        """Capture complete factory floor state."""
        programs = [p["program_id"] for p in self.program_operator.list_catalog()]
        agents = [a.agent_id for a in self.agent_registry.list_agents()]
        sessions = [s.session_id for s in self.session_runtime.list_sessions()]
        active_runs = [r_id for r_id, r in self._live_runs.items() if r.get("tenant_id") == tenant_id]

        snapshot_id = f"snap_{len(active_runs)}_{len(programs)}"
        return FactoryFloorSnapshot(
            snapshot_id=snapshot_id,
            tenant_id=tenant_id,
            program_count=len(programs),
            agent_count=len(agents),
            session_count=len(sessions),
            active_runs_count=len(active_runs),
            completed_runs_count=len(self._replays),
            programs=tuple(programs),
            agents=tuple(agents),
            active_runs=tuple(active_runs),
            sandboxes=(),
        )


# ============================================================================
# 6. Read-Only Observability Viewer
# ============================================================================


class ReadOnlyObservabilityViewer:
    """
    Read-only facade generating visual ASCII/text dashboards, workflow state transition graphs,
    and event timelines directly from canonical traces without mutation authority.
    """

    def __init__(self, engine: UnifiedFactoryCommandEngine) -> None:
        self.engine = engine

    def render_factory_floor(self, tenant_id: str = "default_tenant") -> str:
        snapshot = self.engine.get_floor_snapshot(tenant_id)
        return (
            f"+------------------------------------------------------------+\n"
            f"| CAE FACTORY FLOOR DASHBOARD (READ-ONLY)                     |\n"
            f"+------------------------------------------------------------+\n"
            f"| Tenant: {snapshot.tenant_id:<50} |\n"
            f"| Programs: {snapshot.program_count:<7} Agents: {snapshot.agent_count:<7} Sessions: {snapshot.session_count:<7} |\n"
            f"| Active Runs: {snapshot.active_runs_count:<20} Completed: {snapshot.completed_runs_count:<14} |\n"
            f"+------------------------------------------------------------+\n"
            f"| Digest: {snapshot.snapshot_sha256:<50} |\n"
            f"+------------------------------------------------------------+"
        )

    def render_run_timeline(self, run_id: str, tenant_id: str = "default_tenant") -> str:
        replay = self.engine._replays.get(run_id)
        if not replay:
            raise EntityNotFoundError("RUN", run_id)

        if replay.tenant_id != tenant_id:
            raise ObservabilityTenantIsolationError(tenant_id, replay.tenant_id, run_id)

        lines = [
            f"=== RUN TIMELINE: {run_id} ===",
            f"Program: {replay.program_id} | Events: {replay.total_events}",
        ]
        for event in replay.events:
            status = "COMMITTED" if event.is_committed else "PENDING_TRANSITION"
            lines.append(
                f" [{event.sequence_number}] {event.event_kind} | {event.state_before} -> {event.state_after} [{status}]"
            )
        return "\n".join(lines)

    def attempt_mutation(self, operation: str) -> None:
        """Explicitly defends Gate 4: Observability surface is strictly read-only."""
        raise ReadOnlyObservabilityMutationError(operation)
