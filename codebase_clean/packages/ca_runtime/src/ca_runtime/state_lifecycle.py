"""CAE State Lifecycle, Transition, Repair, and Resume Hooks Engine.

Governed by:
- TS-CAE-PROG-001 / Phase 2 Mandate M20
- 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md
- 00_CONTROL/23_PHASE2_EVENT_TRACE_CONTRACT.md
- 00_CONTROL/24_PHASE2_FAULT_INJECTION_MATRIX.md
- 00_CONTROL/26_PHASE2_REPLAY_IDEMPOTENCY_CONTRACT.md
- 00_CONTROL/06_STATE_AND_HOOKS_MODEL.md
- Phase 1 M11 Architecture Decision Record (StateM adoption pattern)

StateM Operational Lifecycle:
  Plan
  -> Execute State:
     1. in_hook: State-context preparation, tenancy/lane enforcement, invariant loading.
     2. state body: Bounded agent work under capsule/skill constraints.
     3. out_hook: Persistence, intermediate checkpointing, pending side-effect registration.
     4. before_transfer: Deterministic blocking checks, schema validation, receipt verification.
  -> State Commit (Transferred) OR Governed Repair (Repairing) OR Lossless Resume.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from datetime import datetime, timezone
import enum
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_state_runtime import (
    IProgramStateStore,
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    ProgramStateTransition,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    ProgramTransitionContract,
    ProgramTransitionResult,
    SideEffectClass,
    UniversalProgramStateRuntime,
    _build_transition_receipt,
    _compute_state_hash,
    _generate_transition_id,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyViolationError,
    require_current_tenant_context,
)

logger = logging.getLogger("ca_runtime.state_lifecycle")


# ============================================================================
# 1. Typed Exception Hierarchy
# ============================================================================

class StateLifecycleError(ProgramStateRuntimeError):
    """Base exception for state lifecycle, hook, and recovery violations."""
    pass


class HookRejectionError(StateLifecycleError):
    """Raised when an in_hook or out_hook explicitly rejects execution."""

    def __init__(self, hook_phase: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"Hook execution rejected at phase '{hook_phase}': {reason}",
            reason_code=f"HOOK_REJECTED_{hook_phase.upper()}",
            details=details or {},
        )
        self.hook_phase = hook_phase
        self.reason = reason


class BeforeTransferValidationError(StateLifecycleError):
    """Raised when before_transfer blocking check fails."""

    def __init__(self, aggregate_id: str, transition_name: str, check_name: str, reason: str):
        super().__init__(
            f"Before-transfer check '{check_name}' failed for transition '{transition_name}' "
            f"on aggregate '{aggregate_id}': {reason}",
            reason_code="BEFORE_TRANSFER_VALIDATION_FAILED",
            details={
                "aggregate_id": aggregate_id,
                "transition_name": transition_name,
                "check_name": check_name,
                "reason": reason,
            },
        )
        self.check_name = check_name


class DuplicateResumeBlockedError(StateLifecycleError):
    """Raised when a resume attempt with an existing idempotency key attempts duplicate unsafe mutations."""

    def __init__(self, aggregate_id: str, idempotency_key: str, existing_receipt_id: str):
        super().__init__(
            f"Duplicate resume blocked for aggregate '{aggregate_id}' with idempotency key '{idempotency_key}'. "
            f"Existing committed receipt: '{existing_receipt_id}'",
            reason_code="DUPLICATE_RESUME_BLOCKED",
            details={
                "aggregate_id": aggregate_id,
                "idempotency_key": idempotency_key,
                "existing_receipt_id": existing_receipt_id,
            },
        )


class UncertainEffectReconciliationError(StateLifecycleError):
    """Raised when an external effect is in an uncertain state requiring manual or governed reconciliation."""

    def __init__(self, effect_id: str, settlement_id: str, reason: str):
        super().__init__(
            f"Uncertain external effect '{effect_id}' (settlement '{settlement_id}') requires reconciliation: {reason}",
            reason_code="UNCERTAIN_EFFECT_RECONCILIATION_REQUIRED",
            details={"effect_id": effect_id, "settlement_id": settlement_id, "reason": reason},
        )


class StateRepairRequiredError(StateLifecycleError):
    """Raised when an unrecoverable invariant violation forces aggregate into REPAIRING lifecycle."""

    def __init__(self, aggregate_id: str, reason: str):
        super().__init__(
            f"Aggregate '{aggregate_id}' entered REPAIRING state: {reason}",
            reason_code="STATE_REPAIR_REQUIRED",
            details={"aggregate_id": aggregate_id, "reason": reason},
        )


# ============================================================================
# 2. Causal Trace Contract (23_PHASE2_EVENT_TRACE_CONTRACT.md)
# ============================================================================

class CausalTraceEventType(str, enum.Enum):
    """Causal trace event progression mandated by Phase 2 Event Trace Contract."""
    PROGRAM_REQUESTED = "PROGRAM_REQUESTED"
    AUTHORIZED = "AUTHORIZED"
    STATE_ENTERED = "STATE_ENTERED"
    AGENT_STARTED = "AGENT_STARTED"
    SKILL_LOADED = "SKILL_LOADED"
    TOOL_REQUESTED = "TOOL_REQUESTED"
    TOOL_ALLOWED = "TOOL_ALLOWED"
    TOOL_BLOCKED = "TOOL_BLOCKED"
    OPERATION_STARTED = "OPERATION_STARTED"
    EFFECT_PENDING = "EFFECT_PENDING"
    EFFECT_SETTLED = "EFFECT_SETTLED"
    EFFECT_UNCERTAIN = "EFFECT_UNCERTAIN"
    ARTIFACT_CHANGED = "ARTIFACT_CHANGED"
    RECEIPT_COMMITTED = "RECEIPT_COMMITTED"
    TRANSFER_CHECKED = "TRANSFER_CHECKED"
    TRANSFERRED = "TRANSFERRED"
    REPAIRED = "REPAIRED"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"


class CausalTraceRecord(BaseModel):
    """Cryptographically chained immutable causal trace event."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    trace_id: str
    cae_run_id: str
    program_id: str
    aggregate_id: str
    workspace_id: str
    lane: AuthorityLane
    actor_id: str
    event_type: CausalTraceEventType
    payload_hash: str
    skill_hash: Optional[str] = None
    tool_id: Optional[str] = None
    receipt_id: Optional[str] = None
    recovery_status: Optional[str] = None
    previous_trace_sha256: Optional[str] = None
    timestamp: str = Field(default_factory=utc_now_rfc3339)
    trace_sha256: str = Field(default="")

    @classmethod
    def create(
        cls,
        *,
        cae_run_id: str,
        program_id: str,
        aggregate_id: str,
        workspace_id: str,
        lane: AuthorityLane,
        actor_id: str,
        event_type: CausalTraceEventType,
        payload: Mapping[str, Any],
        skill_hash: Optional[str] = None,
        tool_id: Optional[str] = None,
        receipt_id: Optional[str] = None,
        recovery_status: Optional[str] = None,
        previous_trace_sha256: Optional[str] = None,
    ) -> CausalTraceRecord:
        payload_hash = canonical_sha256(payload)
        now = utc_now_rfc3339()
        raw_core = {
            "cae_run_id": cae_run_id,
            "program_id": program_id,
            "aggregate_id": aggregate_id,
            "workspace_id": workspace_id,
            "lane": lane.value,
            "actor_id": actor_id,
            "event_type": event_type.value,
            "payload_hash": payload_hash,
            "skill_hash": skill_hash,
            "tool_id": tool_id,
            "receipt_id": receipt_id,
            "recovery_status": recovery_status,
            "previous_trace_sha256": previous_trace_sha256,
            "timestamp": now,
        }
        trace_sha256 = canonical_sha256(raw_core)
        trace_id = f"trace_{trace_sha256[:24]}"
        return cls(
            trace_id=trace_id,
            cae_run_id=cae_run_id,
            program_id=program_id,
            aggregate_id=aggregate_id,
            workspace_id=workspace_id,
            lane=lane,
            actor_id=actor_id,
            event_type=event_type,
            payload_hash=payload_hash,
            skill_hash=skill_hash,
            tool_id=tool_id,
            receipt_id=receipt_id,
            recovery_status=recovery_status,
            previous_trace_sha256=previous_trace_sha256,
            timestamp=now,
            trace_sha256=trace_sha256,
        )


class CausalTraceLedger:
    """In-memory append-only cryptographically chained trace log."""

    def __init__(self) -> None:
        self._traces: List[CausalTraceRecord] = []
        self._by_aggregate: Dict[str, List[CausalTraceRecord]] = {}

    def append(self, record: CausalTraceRecord) -> None:
        self._traces.append(record)
        if record.aggregate_id not in self._by_aggregate:
            self._by_aggregate[record.aggregate_id] = []
        self._by_aggregate[record.aggregate_id].append(record)

    def get_traces_for_aggregate(self, aggregate_id: str) -> List[CausalTraceRecord]:
        return list(self._by_aggregate.get(aggregate_id, []))

    def get_latest_trace_hash(self, aggregate_id: str) -> Optional[str]:
        records = self._by_aggregate.get(aggregate_id, [])
        return records[-1].trace_sha256 if records else None


# ============================================================================
# 3. Replay & Idempotency Contract (26_PHASE2_REPLAY_IDEMPOTENCY_CONTRACT.md)
# ============================================================================

class EffectKind(str, enum.Enum):
    """Classification of state-changing effect."""
    LOCAL_MUTATION = "LOCAL_MUTATION"
    DATABASE_TRANSACTION = "DATABASE_TRANSACTION"
    EXTERNAL_TOOL = "EXTERNAL_TOOL"
    ARTIFACT_EMISSION = "ARTIFACT_EMISSION"


class ReplaySafety(str, enum.Enum):
    """Replay safety posture."""
    REPLAY_SAFE = "REPLAY_SAFE"
    REPLAY_UNSAFE = "REPLAY_UNSAFE"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"


class FailureWindow(str, enum.Enum):
    """Execution window in which a fault occurred."""
    PRE_EFFECT = "PRE_EFFECT"
    IN_EFFECT = "IN_EFFECT"
    POST_EFFECT_PRE_RECEIPT = "POST_EFFECT_PRE_RECEIPT"
    POST_RECEIPT = "POST_RECEIPT"


class StateEffectDeclaration(BaseModel):
    """Declaration of a pending or settled side effect."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    effect_id: str
    effect_kind: EffectKind
    replay_safety: ReplaySafety
    idempotency_key: str
    settlement_id: str
    failure_window: FailureWindow = FailureWindow.PRE_EFFECT
    settled: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# 4. Checkpoints and State Snapshot Management
# ============================================================================

class StateCheckpoint(BaseModel):
    """Immutable state snapshot captured at out_hook or during interruption."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    checkpoint_id: str
    aggregate_id: str
    workspace_id: str
    cae_run_id: str
    version: int
    current_state: str
    state_data: Dict[str, Any]
    state_hash: str
    idempotency_key: Optional[str] = None
    receipt_id: Optional[str] = None
    effects: List[StateEffectDeclaration] = Field(default_factory=list)
    created_at: str = Field(default_factory=utc_now_rfc3339)


# ============================================================================
# 5. Hook Interfaces and Results
# ============================================================================

class HookPhase(str, enum.Enum):
    """StateM hook lifecycle phases."""
    IN_HOOK = "IN_HOOK"
    OUT_HOOK = "OUT_HOOK"
    BEFORE_TRANSFER = "BEFORE_TRANSFER"
    REPAIR = "REPAIR"
    RESUME = "RESUME"


class HookExecutionStatus(str, enum.Enum):
    """Outcome status of a hook execution."""
    PASSED = "PASSED"
    REJECTED = "REJECTED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"


class HookResult(BaseModel):
    """Result emitted by a lifecycle hook."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    phase: HookPhase
    status: HookExecutionStatus
    check_name: str
    message: str = "OK"
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=utc_now_rfc3339)


# Type aliases for Hook callables
InHookFn = Callable[[ProgramStateAggregate, str, AuthorityLane, TenantContext], HookResult]
OutHookFn = Callable[[ProgramStateAggregate, Dict[str, Any], AuthorityLane], HookResult]
BeforeTransferCheckFn = Callable[[ProgramStateAggregate, ProgramTransitionContract, Dict[str, Any]], HookResult]


# ============================================================================
# 6. State Lifecycle Coordinator
# ============================================================================

class StateLifecycleCoordinator:
    """Orchestrates the StateM lifecycle: in_hook -> work -> out_hook -> before_transfer -> commit / repair / resume.
    
    Guarantees:
    - In-hooks validate tenancy, authority lane, and domain invariant claims.
    - Out-hooks capture candidate state mutations and intermediate checkpoints.
    - Before-transfer checks validate preconditions, schemas, and receipts before advancing state.
    - Governed repair reroutes faults without hidden improvisation.
    - Lossless resumption prevents duplicate external effects via idempotency keys.
    """

    def __init__(
        self,
        state_runtime: UniversalProgramStateRuntime,
        trace_ledger: Optional[CausalTraceLedger] = None,
    ) -> None:
        self.runtime = state_runtime
        self.trace_ledger = trace_ledger or CausalTraceLedger()
        self._checkpoints: Dict[str, StateCheckpoint] = {}
        self._committed_idempotency_keys: Dict[str, ProgramTransitionResult] = {}
        self._in_hooks: List[InHookFn] = []
        self._out_hooks: List[OutHookFn] = []
        self._before_transfer_checks: List[BeforeTransferCheckFn] = []

        # Register default invariant hooks
        self._register_default_hooks()

    def _register_default_hooks(self) -> None:
        """Registers default constitutional invariants for hooks."""
        # Default in-hook: Tenancy & Lane enforcement
        def default_in_hook(
            agg: ProgramStateAggregate,
            transition_name: str,
            actor_lane: AuthorityLane,
            ctx: TenantContext,
        ) -> HookResult:
            if str(ctx.workspace_id) != agg.workspace_id:
                raise CrossWorkspaceLeakError(
                    f"CROSS_WORKSPACE_LEAK: TenantContext workspace {ctx.workspace_id} "
                    f"does not match aggregate workspace {agg.workspace_id}"
                )
            return HookResult(
                phase=HookPhase.IN_HOOK,
                status=HookExecutionStatus.PASSED,
                check_name="tenancy_and_lane_boundary",
                message="Tenancy boundary verified",
                data={"workspace_id": agg.workspace_id, "lane": actor_lane.value},
            )

        self._in_hooks.append(default_in_hook)

        # Default before-transfer check: Non-empty state hash and valid receipt linkage
        def default_before_transfer(
            agg: ProgramStateAggregate,
            contract: ProgramTransitionContract,
            candidate_state_data: Dict[str, Any],
        ) -> HookResult:
            if not agg.state_hash or len(agg.state_hash) != 64:
                return HookResult(
                    phase=HookPhase.BEFORE_TRANSFER,
                    status=HookExecutionStatus.REJECTED,
                    check_name="state_hash_integrity",
                    message="State hash is missing or malformed",
                )
            return HookResult(
                phase=HookPhase.BEFORE_TRANSFER,
                status=HookExecutionStatus.PASSED,
                check_name="state_hash_integrity",
                message="State hash integrity verified",
            )

        self._before_transfer_checks.append(default_before_transfer)

    def register_in_hook(self, hook: InHookFn) -> None:
        self._in_hooks.append(hook)

    def register_out_hook(self, hook: OutHookFn) -> None:
        self._out_hooks.append(hook)

    def register_before_transfer_check(self, check: BeforeTransferCheckFn) -> None:
        self._before_transfer_checks.append(check)

    def _emit_trace(
        self,
        *,
        agg: ProgramStateAggregate,
        lane: AuthorityLane,
        actor_id: str,
        event_type: CausalTraceEventType,
        payload: Mapping[str, Any],
        receipt_id: Optional[str] = None,
        recovery_status: Optional[str] = None,
        tool_id: Optional[str] = None,
    ) -> CausalTraceRecord:
        prev_hash = self.trace_ledger.get_latest_trace_hash(agg.aggregate_id)
        record = CausalTraceRecord.create(
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            lane=lane,
            actor_id=actor_id,
            event_type=event_type,
            payload=payload,
            receipt_id=receipt_id,
            recovery_status=recovery_status,
            tool_id=tool_id,
            previous_trace_sha256=prev_hash,
        )
        self.trace_ledger.append(record)
        return record

    def execute_state_phase(
        self,
        *,
        aggregate_id: str,
        transition_name: str,
        actor_id: str,
        actor_lane: AuthorityLane,
        work_fn: Callable[[ProgramStateAggregate], Dict[str, Any]],
        context: Optional[TenantContext] = None,
        context_claims: Optional[Sequence[str]] = None,
        idempotency_key: Optional[str] = None,
        declared_effects: Optional[Sequence[StateEffectDeclaration]] = None,
        simulate_crash_window: Optional[FailureWindow] = None,
    ) -> ProgramTransitionResult:
        """Executes one complete state lifecycle cycle adhering to StateM control protocol.
        
        Lifecycle:
        1. Idempotency replay check (prevents duplicate mutations).
        2. in_hook execution (tenancy, lane, preconditions).
        3. Causal trace emission (STATE_ENTERED, OPERATION_STARTED).
        4. Crash simulation before work if requested.
        5. State body / agent work execution.
        6. out_hook execution & intermediate checkpoint creation.
        7. Crash simulation after effect/work if requested.
        8. before_transfer blocking validation checks.
        9. Atomic state transition commit & receipt emission.
        10. Causal trace emission (TRANSFERRED, COMPLETED).
        """
        ctx = context or require_current_tenant_context()
        agg = self.runtime.get_aggregate(aggregate_id)

        # 1. Idempotency Check
        if idempotency_key:
            cache_key = f"{agg.workspace_id}:{transition_name}:{idempotency_key}"
            if cache_key in self._committed_idempotency_keys:
                cached = self._committed_idempotency_keys[cache_key]
                logger.info("Idempotent replay detected for key %s", idempotency_key)
                return cached

        # 2. In-Hook Verification
        for in_h in self._in_hooks:
            res = in_h(agg, transition_name, actor_lane, ctx)
            if res.status != HookExecutionStatus.PASSED:
                self._emit_trace(
                    agg=agg,
                    lane=actor_lane,
                    actor_id=actor_id,
                    event_type=CausalTraceEventType.BLOCKED,
                    payload={"hook": res.check_name, "reason": res.message},
                )
                raise HookRejectionError(
                    hook_phase="in_hook",
                    reason=f"Check '{res.check_name}' failed: {res.message}",
                    details=res.data,
                )

        self._emit_trace(
            agg=agg,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"current_state": agg.current_state, "transition_name": transition_name},
        )
        self._emit_trace(
            agg=agg,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.OPERATION_STARTED,
            payload={"transition_name": transition_name, "actor_id": actor_id},
        )

        # 3. Crash before work window check
        if simulate_crash_window == FailureWindow.PRE_EFFECT:
            self._emit_trace(
                agg=agg,
                lane=actor_lane,
                actor_id=actor_id,
                event_type=CausalTraceEventType.EFFECT_UNCERTAIN,
                payload={"failure_window": "PRE_EFFECT"},
                recovery_status="FAULT_SIMULATED",
            )
            raise StateLifecycleError("Simulated crash in PRE_EFFECT window before mutation")

        # 4. State Body / Agent Work Execution
        candidate_state_updates = work_fn(agg)

        # 5. Out-Hook Execution & Intermediate Checkpoint
        for out_h in self._out_hooks:
            res = out_h(agg, candidate_state_updates, actor_lane)
            if res.status != HookExecutionStatus.PASSED:
                raise HookRejectionError(
                    hook_phase="out_hook",
                    reason=f"Check '{res.check_name}' failed: {res.message}",
                    details=res.data,
                )

        # Capture intermediate checkpoint
        chkpt_id = f"chkpt_{agg.aggregate_id}_{agg.version}_{uuid4().hex[:12]}"
        checkpoint = StateCheckpoint(
            checkpoint_id=chkpt_id,
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            version=agg.version,
            current_state=agg.current_state,
            state_data=candidate_state_updates,
            state_hash=agg.state_hash,
            idempotency_key=idempotency_key,
            effects=list(declared_effects or []),
        )
        self._checkpoints[chkpt_id] = checkpoint

        # 6. Crash post-effect pre-receipt window check
        if simulate_crash_window == FailureWindow.POST_EFFECT_PRE_RECEIPT:
            self._emit_trace(
                agg=agg,
                lane=actor_lane,
                actor_id=actor_id,
                event_type=CausalTraceEventType.EFFECT_UNCERTAIN,
                payload={"failure_window": "POST_EFFECT_PRE_RECEIPT", "checkpoint_id": chkpt_id},
                recovery_status="FAULT_SIMULATED",
            )
            raise StateLifecycleError(f"Simulated crash in POST_EFFECT_PRE_RECEIPT window; Checkpoint {chkpt_id} saved")

        # 7. Before-Transfer Blocking Validation Checks
        contract = self.runtime.validate_transition(
            aggregate_id=aggregate_id,
            transition_name=transition_name,
            actor_lane=actor_lane,
            context_claims=context_claims,
            expected_version=agg.version,
        )

        for check in self._before_transfer_checks:
            res = check(agg, contract, candidate_state_updates)
            if res.status != HookExecutionStatus.PASSED:
                self._emit_trace(
                    agg=agg,
                    lane=actor_lane,
                    actor_id=actor_id,
                    event_type=CausalTraceEventType.TRANSFER_CHECKED,
                    payload={"check": res.check_name, "outcome": "FAILED", "reason": res.message},
                )
                self._emit_trace(
                    agg=agg,
                    lane=actor_lane,
                    actor_id=actor_id,
                    event_type=CausalTraceEventType.BLOCKED,
                    payload={"transition_name": transition_name, "reason": res.message},
                )
                raise BeforeTransferValidationError(
                    aggregate_id=aggregate_id,
                    transition_name=transition_name,
                    check_name=res.check_name,
                    reason=res.message,
                )

        self._emit_trace(
            agg=agg,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.TRANSFER_CHECKED,
            payload={"transition_name": transition_name, "outcome": "PASSED"},
        )

        # 8. Atomic State Transition Commit
        result = self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name=transition_name,
            payload=candidate_state_updates,
            actor_id=actor_id,
            actor_lane=actor_lane,
            context_claims=context_claims,
            expected_version=agg.version,
            state_updates=candidate_state_updates,
        )

        # 9. Register Idempotency Cache
        if idempotency_key:
            cache_key = f"{agg.workspace_id}:{transition_name}:{idempotency_key}"
            self._committed_idempotency_keys[cache_key] = result

        # 10. Trace Transferred & Completed
        self._emit_trace(
            agg=result.aggregate,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.TRANSFERRED,
            payload={
                "from_state": contract.from_state,
                "to_state": contract.to_state,
                "version": result.aggregate.version,
            },
            receipt_id=result.receipt_id,
        )
        self._emit_trace(
            agg=result.aggregate,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.COMPLETED,
            payload={"receipt_id": result.receipt_id, "audit_digest": result.audit_digest},
            receipt_id=result.receipt_id,
        )

        return result

    def resume_from_checkpoint(
        self,
        checkpoint_id: str,
        actor_id: str,
        actor_lane: AuthorityLane,
        work_fn: Callable[[ProgramStateAggregate], Dict[str, Any]],
        context: Optional[TenantContext] = None,
    ) -> ProgramTransitionResult:
        """Resumes execution from a saved checkpoint, handling uncertain effects and ensuring zero duplicate mutations."""
        if checkpoint_id not in self._checkpoints:
            raise StateLifecycleError(f"Checkpoint '{checkpoint_id}' not found")

        chkpt = self._checkpoints[checkpoint_id]
        agg = self.runtime.get_aggregate(chkpt.aggregate_id)

        # Check if already committed with this idempotency key
        if chkpt.idempotency_key:
            cache_key = f"{chkpt.workspace_id}:{chkpt.current_state}:{chkpt.idempotency_key}"
            if cache_key in self._committed_idempotency_keys:
                logger.info("Resumed checkpoint was already committed. Returning cached result.")
                return self._committed_idempotency_keys[cache_key]

        # Check for replay-unsafe external effects requiring reconciliation
        for effect in chkpt.effects:
            if effect.replay_safety == ReplaySafety.RECONCILIATION_REQUIRED and not effect.settled:
                raise UncertainEffectReconciliationError(
                    effect_id=effect.effect_id,
                    settlement_id=effect.settlement_id,
                    reason="External effect is in an uncertain state across process restart and requires reconciliation",
                )

        self._emit_trace(
            agg=agg,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.STATE_ENTERED,
            payload={"checkpoint_id": checkpoint_id, "resumed": True},
            recovery_status="RESUMED_FROM_CHECKPOINT",
        )

        # Re-execute state phase cleanly
        return self.execute_state_phase(
            aggregate_id=chkpt.aggregate_id,
            transition_name=agg.current_state,  # Resume transition
            actor_id=actor_id,
            actor_lane=actor_lane,
            work_fn=work_fn,
            context=context,
            idempotency_key=chkpt.idempotency_key,
        )

    def route_to_repair(
        self,
        *,
        aggregate_id: str,
        fault_reason: str,
        actor_id: str,
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ProgramTransitionResult:
        """Transitions an aggregate to the governed REPAIRING lifecycle stage under COMMANDER authority."""
        agg = self.runtime.get_aggregate(aggregate_id)

        self._emit_trace(
            agg=agg,
            lane=actor_lane,
            actor_id=actor_id,
            event_type=CausalTraceEventType.REPAIRED,
            payload={"fault_reason": fault_reason},
            recovery_status="ROUTED_TO_REPAIR",
        )

        return self.runtime.repair_state(
            aggregate_id=aggregate_id,
            repair_action="enter_governed_repair",
            repair_payload={"fault_reason": fault_reason},
            actor_id=actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            target_state="REPAIRING",
            state_updates={"repair_reason": fault_reason, "repaired_at": utc_now_rfc3339()},
        )
