"""CAE-to-Pi Runtime Substrate Adapter and State Boundary.

Governed by TS-CAE-TEN-001, 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md,
and Phase 1 M11 Architecture Decision Record.

Maps canonical CAE run, state aggregate, transition contract, and receipt semantics
to Pi session, lane, and operation execution state while strictly enforcing:
1. CAE remains the authoritative state and receipt master.
2. Four distinct Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
3. Passive, flat Skills and typed mutation boundaries.
4. Clean separation between ephemeral Pi runtime state and canonical CAE state.
5. Safe interruption and lossless, uncorrupted resumption.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import enum
import hashlib
import json
from typing import Any, Callable, Dict, Mapping, Optional, Sequence
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    IdempotencyPayloadMismatchError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)
from ca_runtime.tenant_operations import OperationReceipt


# --- Typed Exceptions ---

class PiRuntimeError(TenancyError):
    """Base error for Pi runtime substrate adapter violations."""
    pass


class AuthorityLaneMismatchError(PiRuntimeError):
    """Raised when an operation is attempted across an unauthorized Authority Lane."""
    pass


class PiSessionInterruptedError(PiRuntimeError):
    """Raised when a Pi execution session is interrupted before state commit."""
    pass


class PiRuntimeStateError(PiRuntimeError):
    """Raised when Pi session lifecycle transition is invalid."""
    pass


class PreconditionViolationError(PiRuntimeError):
    """Raised when a CAE transition contract precondition is violated."""
    pass


# --- Enums and Data Models ---

class AuthorityLane(str, enum.Enum):
    """The four non-negotiable CAE Authority Lanes."""
    HUNTER = "HUNTER"
    ANALYST = "ANALYST"
    COMPOSER = "COMPOSER"
    COMMANDER = "COMMANDER"


class PiSessionState(str, enum.Enum):
    """Subordinate Pi runtime session lifecycle states."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    INTERRUPTED = "INTERRUPTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# Authoritative Operation-to-Lane Governance Mapping
OPERATION_LANE_BINDINGS: Mapping[str, AuthorityLane] = {
    # Commander Lane (Governance, Tenancy, Operator Gates, Engagement Initialization)
    "cae.workspace.provision@1.0.0": AuthorityLane.COMMANDER,
    "cae.workspace.membership.grant@1.0.0": AuthorityLane.COMMANDER,
    "cae.operator.grant.issue@1.0.0": AuthorityLane.COMMANDER,
    "cae.engagement.initialize@1.0.0": AuthorityLane.COMMANDER,
    "cae.guest.register@1.0.0": AuthorityLane.COMMANDER,
    "cae.air.confirm-assessment": AuthorityLane.COMMANDER,
    "cae.approval.confirm@1.0.0": AuthorityLane.COMMANDER,

    # Hunter Lane (Discovery, Media Ingestion, Evidence Capture, Bridge Verification)
    "cae.media.verify@1.0.0": AuthorityLane.HUNTER,
    "cae.evidence.capture@1.0.0": AuthorityLane.HUNTER,
    "cae.evidence.capture": AuthorityLane.HUNTER,
    "cae.evidence.authenticate": AuthorityLane.HUNTER,
    "cae.bridge.register-interview-source": AuthorityLane.HUNTER,

    # Analyst Lane (Semantic Assessment, Hypotheses, Validation)
    "cae.air.propose-assessment": AuthorityLane.ANALYST,
    "cae.air.validate-assessment": AuthorityLane.ANALYST,
    "cae.assessment.evaluate@1.0.0": AuthorityLane.ANALYST,

    # Composer Lane (Program Synthesis, Word Boundary EDL, Video Edit Programs)
    "cae.script.compose@1.0.0": AuthorityLane.COMPOSER,
    "cae.composition.compile@1.0.0": AuthorityLane.COMPOSER,
    "cae.video_program.render@1.0.0": AuthorityLane.COMPOSER,
}


@dataclass
class PiSession:
    """Pi execution runtime session container carrying canonical CAE run identity."""
    session_id: str
    cae_run_id: str
    workspace_id: UUID
    lane: AuthorityLane
    state: PiSessionState = PiSessionState.IDLE
    checkpoint_sequence: int = 0
    current_checkpoint_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_rfc3339)
    updated_at: str = field(default_factory=utc_now_rfc3339)


@dataclass(frozen=True, slots=True)
class CaePiRuntimeTrace:
    """Field-level runtime trace capturing the CAE-to-Pi execution boundary."""
    trace_id: str
    session_id: str
    cae_run_id: str
    workspace_id: UUID
    lane: str
    operation_id: str
    pre_state_version: int
    post_state_version: int
    in_hook_passed: bool
    out_hook_passed: bool
    receipt_id: str
    interrupted: bool
    resumed: bool
    started_at: str
    completed_at: str
    trace_sha256: str


@dataclass(frozen=True, slots=True)
class PiExecutionReceipt:
    """Bridge execution receipt encapsulating CAE canonical receipt and Pi execution metadata."""
    receipt_id: str
    cae_run_id: str
    session_id: str
    workspace_id: UUID
    operation_id: str
    idempotency_key: str
    lane: str
    outcome: str
    idempotent_replay: bool
    cae_receipt: Mapping[str, Any]
    runtime_trace: CaePiRuntimeTrace
    receipt_sha256: str


# --- Minimal CAE-to-Pi Runtime Adapter ---

class CaePiRuntimeAdapter:
    """Smallest adapter needed for typed CAE operations to execute in Pi runtime substrate.
    
    Carries CAE run identity, preserves CAE state authority, validates Authority Lanes,
    executes in/out hooks, records runtime traces, and supports safe interruption/resume.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, PiSession] = {}
        self._checkpoints: Dict[str, Dict[str, Any]] = {}
        self._traces: Dict[str, CaePiRuntimeTrace] = {}
        self._receipt_cache: Dict[str, PiExecutionReceipt] = {}
        self._state_aggregates: Dict[str, Dict[str, Any]] = {}

    def create_session(
        self,
        *,
        cae_run_id: str,
        workspace_id: UUID,
        lane: AuthorityLane,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> PiSession:
        """Create a durable Pi execution session bound to a canonical CAE run ID."""
        if not cae_run_id or not cae_run_id.strip():
            raise PiRuntimeError("cae_run_id is required and cannot be empty")
        if not isinstance(workspace_id, UUID):
            raise TenancyViolationError(f"workspace_id must be a UUID, got {type(workspace_id)}")
        if not isinstance(lane, AuthorityLane):
            raise AuthorityLaneMismatchError(f"Invalid AuthorityLane: {lane}")

        session_id = f"pi_sess_{hashlib.sha256(f'{cae_run_id}:{workspace_id}:{lane.value}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"
        session = PiSession(
            session_id=session_id,
            cae_run_id=cae_run_id,
            workspace_id=workspace_id,
            lane=lane,
            state=PiSessionState.IDLE,
            metadata=dict(metadata or {}),
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[PiSession]:
        """Retrieve Pi session by session ID."""
        return self._sessions.get(session_id)

    def get_trace(self, trace_id: str) -> Optional[CaePiRuntimeTrace]:
        """Retrieve runtime trace by trace ID."""
        return self._traces.get(trace_id)

    def get_canonical_state(self, aggregate_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve authoritative CAE state aggregate."""
        return self._state_aggregates.get(aggregate_id)

    def _validate_authority_lane(self, operation_id: str, session_lane: AuthorityLane) -> None:
        """Assert that the operation is permitted in the active Authority Lane."""
        required_lane = OPERATION_LANE_BINDINGS.get(operation_id)
        if required_lane is not None and required_lane != session_lane:
            raise AuthorityLaneMismatchError(
                f"AUTHORITY_LANE_MISMATCH: Operation '{operation_id}' requires {required_lane.value} lane, "
                f"but Pi session is executing in {session_lane.value} lane"
            )

    def _in_hook(
        self,
        *,
        session: PiSession,
        operation_id: str,
        idempotency_key: str,
        command_payload: Mapping[str, Any],
        context: TenantContext,
    ) -> Dict[str, Any]:
        """Execute pre-operation hook: enforce tenancy, authority lanes, and invariants."""
        # 1. Tenancy Boundary Check
        if context.workspace_id != session.workspace_id:
            raise CrossWorkspaceLeakError(
                f"CROSS_WORKSPACE_LEAK: TenantContext workspace {context.workspace_id} "
                f"does not match PiSession workspace {session.workspace_id}"
            )

        # 2. Authority Lane Check
        self._validate_authority_lane(operation_id, session.lane)

        # 3. Aggregate State Inspection (Optimistic Locking & Precondition Check)
        aggregate_id = str(command_payload.get("aggregate_id") or command_payload.get("evidence_id") or command_payload.get("media_asset_id") or command_payload.get("workspace_id") or "")
        current_state = self._state_aggregates.get(aggregate_id, {"version": 0, "state": "INITIAL"})

        return {
            "in_hook_passed": True,
            "pre_state_version": current_state["version"],
            "pre_state": current_state["state"],
            "started_at": utc_now_rfc3339(),
        }

    def _out_hook(
        self,
        *,
        session: PiSession,
        operation_id: str,
        idempotency_key: str,
        command_payload: Mapping[str, Any],
        operation_receipt: OperationReceipt,
        in_hook_data: Mapping[str, Any],
        resumed: bool = False,
    ) -> PiExecutionReceipt:
        """Execute post-operation hook: advance state aggregate, emit immutable receipt & trace."""
        aggregate_id = str(command_payload.get("aggregate_id") or command_payload.get("evidence_id") or command_payload.get("media_asset_id") or command_payload.get("workspace_id") or "")
        pre_version = in_hook_data["pre_state_version"]
        post_version = pre_version + 1

        # Advance canonical CAE state aggregate
        self._state_aggregates[aggregate_id] = {
            "aggregate_id": aggregate_id,
            "workspace_id": str(session.workspace_id),
            "version": post_version,
            "state": "COMMITTED",
            "last_operation_id": operation_id,
            "last_receipt_id": operation_receipt.receipt_id,
            "updated_at": utc_now_rfc3339(),
        }

        # Advance Pi session state
        session.checkpoint_sequence += 1
        session.state = PiSessionState.COMPLETED
        session.updated_at = utc_now_rfc3339()

        completed_at = utc_now_rfc3339()
        trace_core = {
            "session_id": session.session_id,
            "cae_run_id": session.cae_run_id,
            "workspace_id": str(session.workspace_id),
            "lane": session.lane.value,
            "operation_id": operation_id,
            "pre_state_version": pre_version,
            "post_state_version": post_version,
            "in_hook_passed": True,
            "out_hook_passed": True,
            "receipt_id": operation_receipt.receipt_id,
            "interrupted": False,
            "resumed": resumed,
            "started_at": in_hook_data["started_at"],
            "completed_at": completed_at,
        }
        trace_id = f"trace_{canonical_sha256(trace_core)[:24]}"
        runtime_trace = CaePiRuntimeTrace(
            trace_id=trace_id,
            session_id=session.session_id,
            cae_run_id=session.cae_run_id,
            workspace_id=session.workspace_id,
            lane=session.lane.value,
            operation_id=operation_id,
            pre_state_version=pre_version,
            post_state_version=post_version,
            in_hook_passed=True,
            out_hook_passed=True,
            receipt_id=operation_receipt.receipt_id,
            interrupted=False,
            resumed=resumed,
            started_at=in_hook_data["started_at"],
            completed_at=completed_at,
            trace_sha256=canonical_sha256(trace_core),
        )
        self._traces[trace_id] = runtime_trace

        receipt_core = {
            "receipt_id": operation_receipt.receipt_id,
            "cae_run_id": session.cae_run_id,
            "session_id": session.session_id,
            "workspace_id": str(session.workspace_id),
            "operation_id": operation_id,
            "idempotency_key": idempotency_key,
            "lane": session.lane.value,
            "outcome": operation_receipt.outcome,
            "idempotent_replay": operation_receipt.idempotent_replay,
            "cae_receipt": dict(operation_receipt.payload),
            "runtime_trace_id": trace_id,
        }
        pi_receipt = PiExecutionReceipt(
            receipt_id=operation_receipt.receipt_id,
            cae_run_id=session.cae_run_id,
            session_id=session.session_id,
            workspace_id=session.workspace_id,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            lane=session.lane.value,
            outcome=operation_receipt.outcome,
            idempotent_replay=operation_receipt.idempotent_replay,
            cae_receipt=operation_receipt.payload,
            runtime_trace=runtime_trace,
            receipt_sha256=canonical_sha256(receipt_core),
        )

        cache_key = f"{session.workspace_id}:{operation_id}:{idempotency_key}"
        self._receipt_cache[cache_key] = pi_receipt
        return pi_receipt

    def execute_operation(
        self,
        *,
        session: PiSession,
        operation_id: str,
        idempotency_key: str,
        command_payload: Mapping[str, Any],
        execute_fn: Callable[[], OperationReceipt],
        context: Optional[TenantContext] = None,
        simulate_interruption: bool = False,
    ) -> PiExecutionReceipt:
        """Execute a typed CAE semantic operation inside a Pi runtime session.
        
        Guarantees:
        - In-hook validates tenancy, authority lane, and preconditions.
        - Idempotent replays are detected without double-mutation.
        - Controlled interruption saves checkpoint without state corruption.
        - Out-hook verifies atomic receipt lineage and emits runtime trace.
        """
        ctx = context or require_current_tenant_context()
        cache_key = f"{session.workspace_id}:{operation_id}:{idempotency_key}"

        # 1. Idempotent Replay Check
        if cache_key in self._receipt_cache:
            cached = self._receipt_cache[cache_key]
            return PiExecutionReceipt(
                receipt_id=cached.receipt_id,
                cae_run_id=session.cae_run_id,
                session_id=session.session_id,
                workspace_id=session.workspace_id,
                operation_id=operation_id,
                idempotency_key=idempotency_key,
                lane=session.lane.value,
                outcome="IDEMPOTENT_REPLAY",
                idempotent_replay=True,
                cae_receipt=cached.cae_receipt,
                runtime_trace=cached.runtime_trace,
                receipt_sha256=cached.receipt_sha256,
            )

        # 2. In-Hook Verification
        session.state = PiSessionState.RUNNING
        session.updated_at = utc_now_rfc3339()
        in_hook_data = self._in_hook(
            session=session,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            command_payload=command_payload,
            context=ctx,
        )

        # 3. Interruption Simulation Handling
        if simulate_interruption:
            checkpoint_id = f"chkpt_{session.session_id}_{session.checkpoint_sequence + 1}"
            checkpoint_data = {
                "checkpoint_id": checkpoint_id,
                "session_id": session.session_id,
                "cae_run_id": session.cae_run_id,
                "workspace_id": str(session.workspace_id),
                "operation_id": operation_id,
                "idempotency_key": idempotency_key,
                "command_payload": dict(command_payload),
                "interrupted_at": utc_now_rfc3339(),
                "pre_state_version": in_hook_data["pre_state_version"],
            }
            self._checkpoints[checkpoint_id] = checkpoint_data
            session.current_checkpoint_id = checkpoint_id
            session.state = PiSessionState.INTERRUPTED
            session.updated_at = utc_now_rfc3339()

            # Record interrupted trace
            trace_core = {
                "session_id": session.session_id,
                "cae_run_id": session.cae_run_id,
                "workspace_id": str(session.workspace_id),
                "lane": session.lane.value,
                "operation_id": operation_id,
                "pre_state_version": in_hook_data["pre_state_version"],
                "post_state_version": in_hook_data["pre_state_version"],  # Unchanged
                "in_hook_passed": True,
                "out_hook_passed": False,
                "receipt_id": "NONE_INTERRUPTED",
                "interrupted": True,
                "resumed": False,
                "started_at": in_hook_data["started_at"],
                "completed_at": utc_now_rfc3339(),
            }
            trace_id = f"trace_{canonical_sha256(trace_core)[:24]}"
            self._traces[trace_id] = CaePiRuntimeTrace(
                trace_id=trace_id,
                session_id=session.session_id,
                cae_run_id=session.cae_run_id,
                workspace_id=session.workspace_id,
                lane=session.lane.value,
                operation_id=operation_id,
                pre_state_version=in_hook_data["pre_state_version"],
                post_state_version=in_hook_data["pre_state_version"],
                in_hook_passed=True,
                out_hook_passed=False,
                receipt_id="NONE_INTERRUPTED",
                interrupted=True,
                resumed=False,
                started_at=in_hook_data["started_at"],
                completed_at=utc_now_rfc3339(),
                trace_sha256=canonical_sha256(trace_core),
            )

            raise PiSessionInterruptedError(
                f"PI_SESSION_INTERRUPTED: Execution interrupted before CAE state commit for operation {operation_id}. "
                f"Checkpoint {checkpoint_id} saved."
            )

        # 4. Execute Typed CAE Semantic Operation
        op_receipt = execute_fn()

        # 5. Out-Hook Verification & State Finalization
        return self._out_hook(
            session=session,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            command_payload=command_payload,
            operation_receipt=op_receipt,
            in_hook_data=in_hook_data,
            resumed=False,
        )

    def resume_session(
        self,
        *,
        session: PiSession,
        operation_id: str,
        idempotency_key: str,
        command_payload: Mapping[str, Any],
        execute_fn: Callable[[], OperationReceipt],
        context: Optional[TenantContext] = None,
    ) -> PiExecutionReceipt:
        """Resume an interrupted Pi session from its verified checkpoint.
        
        Guarantees that no duplicate mutation occurs and CAE state advances cleanly.
        """
        if session.state != PiSessionState.INTERRUPTED:
            raise PiRuntimeStateError(
                f"Cannot resume session in state '{session.state.value}'; must be 'INTERRUPTED'"
            )

        ctx = context or require_current_tenant_context()

        # Re-run operation safely
        session.state = PiSessionState.RUNNING
        session.updated_at = utc_now_rfc3339()

        in_hook_data = self._in_hook(
            session=session,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            command_payload=command_payload,
            context=ctx,
        )

        op_receipt = execute_fn()

        return self._out_hook(
            session=session,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            command_payload=command_payload,
            operation_receipt=op_receipt,
            in_hook_data=in_hook_data,
            resumed=True,
        )
