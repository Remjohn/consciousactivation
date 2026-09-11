"""Workflow Dispatcher Runtime — CA-M035 / INV-DISP-002.

Orchestrates multi-stage program pipelines with:
  - Idempotency keys: duplicate step execution is refused via a keyed
    fingerprint registry; same key + same payload is a no-op; key collision
    on different payload is a hard error.
  - State rollback: each step's pre-execution snapshot is kept so that on
    failure the dispatcher can revert the aggregate to the known-good point
    before the failing step.
  - Step retry limits: every step declares a max_attempts ceiling; the
    dispatcher enforces it and transitions the pipeline to FAILED_STEP on
    exhaustion.
  - Distributed lease lifecycle tracking: the lease table records
    ACQUIRED → STEP_RUNNING → STEP_COMPLETE (per step) → RELEASED/FAILED;
    re-entrant lease heartbeats keep the lease alive across slow steps.

Authority hierarchy:
  - Caller must hold a RUNNING aggregate produced by CA-M034
    (acquire_execution_lease_and_trigger).
  - COMMANDER lane is required to initiate a dispatch run.
  - ANALYST lane may query step status; HUNTER and COMPOSER are
    read-only observers.

Governing invariant: INV-DISP-002 — no duplicate step execution; state
consistency guaranteed across failures.
"""

from __future__ import annotations

import abc
import enum
import hashlib
import json
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    IProgramStateStore,
    InMemoryProgramStateStore,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateRuntimeError,
)

logger = logging.getLogger("ca_runtime.workflow_dispatch")


# ============================================================================
# 1. Error Taxonomy
# ============================================================================


class WorkflowDispatchError(ProgramStateRuntimeError):
    """Base exception for all Workflow Dispatcher Runtime violations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "WORKFLOW_DISPATCH_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class IdempotencyKeyConflictError(WorkflowDispatchError):
    """Raised when an idempotency key is reused with a different payload.

    Invariant: INV-DISP-002 — duplicate step execution must be prevented.
    A key collision with the *same* payload is a safe no-op; a key collision
    with a *different* payload is a hard error that the caller must resolve
    before proceeding.
    """

    def __init__(
        self,
        step_id: str,
        idempotency_key: str,
        stored_payload_sha: str,
        presented_payload_sha: str,
    ) -> None:
        super().__init__(
            f"Idempotency conflict on step '{step_id}': key '{idempotency_key}' was "
            f"already used with payload sha={stored_payload_sha!r}, "
            f"but presented payload sha={presented_payload_sha!r}",
            reason_code="IDEMPOTENCY_KEY_CONFLICT",
            details={
                "step_id": step_id,
                "idempotency_key": idempotency_key,
                "stored_payload_sha": stored_payload_sha,
                "presented_payload_sha": presented_payload_sha,
            },
        )
        self.step_id = step_id
        self.idempotency_key = idempotency_key
        self.stored_payload_sha = stored_payload_sha
        self.presented_payload_sha = presented_payload_sha


class StepRetryLimitExceededError(WorkflowDispatchError):
    """Raised when a step exceeds its declared max_attempts ceiling.

    Invariant: INV-DISP-002 — guarantees state consistency by refusing to
    allow unbounded retries that could leave the aggregate in an ambiguous
    intermediate state.
    """

    def __init__(self, step_id: str, max_attempts: int, attempt: int) -> None:
        super().__init__(
            f"Step '{step_id}' exceeded retry limit: max_attempts={max_attempts}, "
            f"attempted={attempt}",
            reason_code="STEP_RETRY_LIMIT_EXCEEDED",
            details={
                "step_id": step_id,
                "max_attempts": max_attempts,
                "attempt": attempt,
            },
        )
        self.step_id = step_id
        self.max_attempts = max_attempts
        self.attempt = attempt


class WorkflowLeaseExpiredError(WorkflowDispatchError):
    """Raised when the distributed lease has expired before step completion."""

    def __init__(self, aggregate_id: str, lease_id: str) -> None:
        super().__init__(
            f"Workflow lease '{lease_id}' for aggregate '{aggregate_id}' has expired",
            reason_code="WORKFLOW_LEASE_EXPIRED",
            details={"aggregate_id": aggregate_id, "lease_id": lease_id},
        )
        self.aggregate_id = aggregate_id
        self.lease_id = lease_id


class WorkflowStepNotFoundError(WorkflowDispatchError):
    """Raised when a referenced step ID does not exist in the pipeline."""

    def __init__(self, step_id: str, pipeline_id: str) -> None:
        super().__init__(
            f"Step '{step_id}' not found in pipeline '{pipeline_id}'",
            reason_code="WORKFLOW_STEP_NOT_FOUND",
            details={"step_id": step_id, "pipeline_id": pipeline_id},
        )
        self.step_id = step_id
        self.pipeline_id = pipeline_id


class WorkflowRollbackError(WorkflowDispatchError):
    """Raised when a state rollback cannot be completed safely."""

    def __init__(self, aggregate_id: str, step_id: str, reason: str) -> None:
        super().__init__(
            f"State rollback failed for step '{step_id}' on aggregate '{aggregate_id}': {reason}",
            reason_code="WORKFLOW_ROLLBACK_FAILED",
            details={"aggregate_id": aggregate_id, "step_id": step_id, "reason": reason},
        )
        self.aggregate_id = aggregate_id
        self.step_id = step_id
        self.reason = reason


class WorkflowAuthorityViolationError(WorkflowDispatchError):
    """Raised when a caller attempts a dispatch action from an unauthorized lane."""

    def __init__(self, action: str, actor_lane: AuthorityLane, required_lane: AuthorityLane) -> None:
        super().__init__(
            f"Authority violation for action '{action}': actor lane '{actor_lane.value}' "
            f"does not satisfy required lane '{required_lane.value}'",
            reason_code="WORKFLOW_AUTHORITY_VIOLATION",
            details={
                "action": action,
                "actor_lane": actor_lane.value,
                "required_lane": required_lane.value,
            },
        )
        self.action = action
        self.actor_lane = actor_lane
        self.required_lane = required_lane


class WorkflowAggregatePreconditionError(WorkflowDispatchError):
    """Raised when the aggregate is not in the expected lifecycle state for dispatch."""

    def __init__(self, aggregate_id: str, required: str, actual: str) -> None:
        super().__init__(
            f"Aggregate '{aggregate_id}' must be in lifecycle '{required}' "
            f"to initiate workflow dispatch, but is in '{actual}'",
            reason_code="WORKFLOW_AGGREGATE_PRECONDITION",
            details={
                "aggregate_id": aggregate_id,
                "required_lifecycle": required,
                "actual_lifecycle": actual,
            },
        )
        self.aggregate_id = aggregate_id
        self.required = required
        self.actual = actual


# ============================================================================
# 2. Domain Enums & Value Objects
# ============================================================================


class StepStatus(str, enum.Enum):
    """Lifecycle states for a single pipeline step."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    SKIPPED = "SKIPPED"  # idempotent replay of an already-completed step


class PipelineStatus(str, enum.Enum):
    """Overall pipeline run lifecycle states."""
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class LeaseStatus(str, enum.Enum):
    """Distributed lease lifecycle states (INV-DISP-002)."""
    ACQUIRED = "ACQUIRED"
    HEARTBEAT = "HEARTBEAT"
    STEP_RUNNING = "STEP_RUNNING"
    STEP_COMPLETE = "STEP_COMPLETE"
    RELEASED = "RELEASED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class StepDefinition:
    """Declarative specification for one step in a pipeline.

    Attributes:
        step_id:      Unique identifier within the pipeline.
        step_name:    Human-readable label.
        max_attempts: Maximum execution attempts before the step is failed.
                      Must be >= 1. Default is 1 (no retry).
        rollback_on_failure: When True (default) the dispatcher snapshots
                      aggregate state before the step and rolls back on
                      exhausted retries or unrecoverable error.
        authority_lane: Minimum authority lane required to execute this step.
                      Defaults to COMMANDER.
        metadata:     Arbitrary step-level annotations.
    """
    step_id: str
    step_name: str
    max_attempts: int = 1
    rollback_on_failure: bool = True
    authority_lane: AuthorityLane = AuthorityLane.COMMANDER
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise WorkflowDispatchError(
                f"Step '{self.step_id}' max_attempts must be >= 1, got {self.max_attempts}",
                reason_code="INVALID_STEP_DEFINITION",
                details={"step_id": self.step_id, "max_attempts": self.max_attempts},
            )
        if not self.step_id:
            raise WorkflowDispatchError(
                "step_id must not be empty",
                reason_code="INVALID_STEP_DEFINITION",
            )


@dataclass
class StepExecutionRecord:
    """Mutable record for a single step execution attempt.

    Attributes:
        step_id:          Which step this belongs to.
        attempt:          1-based attempt counter.
        idempotency_key:  Keyed fingerprint; prevents duplicate execution.
        payload_sha:      SHA-256 of the canonical step payload.
        status:           Current step status.
        started_at:       RFC-3339 timestamp.
        completed_at:     RFC-3339 timestamp; None until terminal.
        error_message:    Populated on FAILED status.
        pre_snapshot_sha: SHA-256 of the aggregate state_data *before* the
                          step ran; used by rollback to restore state.
        result:           Arbitrary step output stored on success.
    """
    step_id: str
    attempt: int
    idempotency_key: str
    payload_sha: str
    status: StepStatus = StepStatus.PENDING
    started_at: str = field(default_factory=utc_now_rfc3339)
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    pre_snapshot_sha: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "attempt": self.attempt,
            "idempotency_key": self.idempotency_key,
            "payload_sha": self.payload_sha,
            "status": self.status.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error_message": self.error_message,
            "pre_snapshot_sha": self.pre_snapshot_sha,
            "result": self.result,
        }


@dataclass
class DistributedLeaseRecord:
    """Lifecycle tracking record for the dispatcher's distributed lease.

    Invariant: one pipeline run = one lease record; status must advance
    monotonically through its lifecycle states.
    """
    lease_id: str
    aggregate_id: str
    pipeline_id: str
    actor_id: str
    status: LeaseStatus = LeaseStatus.ACQUIRED
    acquired_at: str = field(default_factory=utc_now_rfc3339)
    last_heartbeat_at: Optional[str] = None
    released_at: Optional[str] = None
    current_step_id: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lease_id": self.lease_id,
            "aggregate_id": self.aggregate_id,
            "pipeline_id": self.pipeline_id,
            "actor_id": self.actor_id,
            "status": self.status.value,
            "acquired_at": self.acquired_at,
            "last_heartbeat_at": self.last_heartbeat_at,
            "released_at": self.released_at,
            "current_step_id": self.current_step_id,
            "error_message": self.error_message,
        }


@dataclass
class PipelineRun:
    """Complete state of one pipeline run.

    Attributes:
        run_id:        Unique run identifier.
        aggregate_id:  Owning ProgramStateAggregate ID.
        pipeline_id:   Which pipeline definition was executed.
        status:        Overall pipeline status.
        steps:         Ordered list of step definitions executed.
        records:       Flat list of all StepExecutionRecord objects (all
                       attempts for all steps).
        lease:         Distributed lease tracking record.
        snapshots:     Keyed by ``{step_id}:{attempt}`` → snapshot of
                       aggregate.state_data serialized as canonical JSON.
                       Populated before each step runs; used for rollback.
        started_at:    RFC-3339 timestamp when the run was created.
        completed_at:  RFC-3339 timestamp when terminal state reached.
    """
    run_id: str
    aggregate_id: str
    pipeline_id: str
    status: PipelineStatus
    steps: List[StepDefinition]
    records: List[StepExecutionRecord] = field(default_factory=list)
    lease: Optional[DistributedLeaseRecord] = None
    snapshots: Dict[str, str] = field(default_factory=dict)
    started_at: str = field(default_factory=utc_now_rfc3339)
    completed_at: Optional[str] = None

    # --- helpers -----------------------------------------------------------

    def step_by_id(self, step_id: str) -> StepDefinition:
        for s in self.steps:
            if s.step_id == step_id:
                return s
        raise WorkflowStepNotFoundError(step_id=step_id, pipeline_id=self.pipeline_id)

    def records_for_step(self, step_id: str) -> List[StepExecutionRecord]:
        return [r for r in self.records if r.step_id == step_id]

    def latest_record_for_step(self, step_id: str) -> Optional[StepExecutionRecord]:
        recs = self.records_for_step(step_id)
        return recs[-1] if recs else None

    def attempt_count(self, step_id: str) -> int:
        return len(self.records_for_step(step_id))


# ============================================================================
# 3. Idempotency Registry
# ============================================================================


class IdempotencyRegistry:
    """Thread-safe idempotency key store.

    Records (step_id, idempotency_key) → payload_sha pairs.
    Lookup rules (INV-DISP-002):
      - First call: record and return ``(False, None)`` meaning "proceed".
      - Same key, same payload sha: return ``(True, record)`` meaning "skip".
      - Same key, different payload sha: raise IdempotencyKeyConflictError.
    """

    def __init__(self) -> None:
        # maps idempotency_key → {"step_id": ..., "payload_sha": ..., "completed_at": ...}
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def check_and_register(
        self,
        step_id: str,
        idempotency_key: str,
        payload_sha: str,
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Check key and register if new.

        Returns:
            (already_done, record) — if ``already_done`` is True the step
            can be safely skipped using ``record`` as the prior result.

        Raises:
            IdempotencyKeyConflictError — same key, different payload.
        """
        with self._lock:
            existing = self._store.get(idempotency_key)
            if existing is None:
                self._store[idempotency_key] = {
                    "step_id": step_id,
                    "payload_sha": payload_sha,
                    "completed_at": None,
                }
                return False, None
            if existing["payload_sha"] != payload_sha:
                raise IdempotencyKeyConflictError(
                    step_id=step_id,
                    idempotency_key=idempotency_key,
                    stored_payload_sha=existing["payload_sha"],
                    presented_payload_sha=payload_sha,
                )
            # Same payload → safe replay
            return True, dict(existing)

    def mark_completed(self, idempotency_key: str, completed_at: str) -> None:
        """Mark an idempotency key as fully completed."""
        with self._lock:
            entry = self._store.get(idempotency_key)
            if entry is not None:
                entry["completed_at"] = completed_at

    def is_registered(self, idempotency_key: str) -> bool:
        """Return True if the key is known to the registry."""
        with self._lock:
            return idempotency_key in self._store


# ============================================================================
# 4. Lease Manager
# ============================================================================


class LeaseManager:
    """Thread-safe distributed lease lifecycle manager.

    Each aggregate_id may hold at most one active lease at a time
    (INV-DISP-002 — one authoritative execution path per aggregate).
    """

    def __init__(self) -> None:
        # aggregate_id → DistributedLeaseRecord
        self._leases: Dict[str, DistributedLeaseRecord] = {}
        self._lock = threading.Lock()

    def acquire(
        self,
        aggregate_id: str,
        pipeline_id: str,
        actor_id: str,
        lease_id: str,
    ) -> DistributedLeaseRecord:
        """Acquire a new dispatch lease.

        Raises:
            WorkflowDispatchError — if a live lease already exists.
        """
        with self._lock:
            existing = self._leases.get(aggregate_id)
            if existing is not None and existing.status not in (
                LeaseStatus.RELEASED,
                LeaseStatus.EXPIRED,
                LeaseStatus.FAILED,
            ):
                raise WorkflowDispatchError(
                    f"Cannot acquire lease: aggregate '{aggregate_id}' already holds "
                    f"an active lease '{existing.lease_id}' in status "
                    f"'{existing.status.value}'",
                    reason_code="LEASE_ALREADY_HELD",
                    details={
                        "aggregate_id": aggregate_id,
                        "existing_lease_id": existing.lease_id,
                        "existing_status": existing.status.value,
                    },
                )
            record = DistributedLeaseRecord(
                lease_id=lease_id,
                aggregate_id=aggregate_id,
                pipeline_id=pipeline_id,
                actor_id=actor_id,
                status=LeaseStatus.ACQUIRED,
                acquired_at=utc_now_rfc3339(),
            )
            self._leases[aggregate_id] = record
            return record

    def heartbeat(self, aggregate_id: str, lease_id: str) -> None:
        """Renew the lease heartbeat to signal the holder is still alive."""
        with self._lock:
            record = self._get_active(aggregate_id, lease_id)
            record.last_heartbeat_at = utc_now_rfc3339()
            record.status = LeaseStatus.HEARTBEAT

    def mark_step_running(self, aggregate_id: str, lease_id: str, step_id: str) -> None:
        """Advance lease status to STEP_RUNNING for the given step."""
        with self._lock:
            record = self._get_active(aggregate_id, lease_id)
            record.current_step_id = step_id
            record.status = LeaseStatus.STEP_RUNNING
            record.last_heartbeat_at = utc_now_rfc3339()

    def mark_step_complete(self, aggregate_id: str, lease_id: str, step_id: str) -> None:
        """Advance lease status to STEP_COMPLETE after a step succeeds."""
        with self._lock:
            record = self._get_active(aggregate_id, lease_id)
            record.current_step_id = step_id
            record.status = LeaseStatus.STEP_COMPLETE
            record.last_heartbeat_at = utc_now_rfc3339()

    def release(self, aggregate_id: str, lease_id: str) -> None:
        """Release the lease; pipeline completed successfully."""
        with self._lock:
            record = self._leases.get(aggregate_id)
            if record is None or record.lease_id != lease_id:
                return
            record.status = LeaseStatus.RELEASED
            record.released_at = utc_now_rfc3339()

    def fail(self, aggregate_id: str, lease_id: str, error_message: str) -> None:
        """Transition the lease to FAILED with an error note."""
        with self._lock:
            record = self._leases.get(aggregate_id)
            if record is None or record.lease_id != lease_id:
                return
            record.status = LeaseStatus.FAILED
            record.error_message = error_message
            record.released_at = utc_now_rfc3339()

    def get(self, aggregate_id: str) -> Optional[DistributedLeaseRecord]:
        """Return the current lease record for an aggregate, or None."""
        with self._lock:
            return self._leases.get(aggregate_id)

    def _get_active(self, aggregate_id: str, lease_id: str) -> DistributedLeaseRecord:
        record = self._leases.get(aggregate_id)
        if record is None or record.lease_id != lease_id:
            raise WorkflowLeaseExpiredError(
                aggregate_id=aggregate_id,
                lease_id=lease_id,
            )
        if record.status in (LeaseStatus.RELEASED, LeaseStatus.EXPIRED, LeaseStatus.FAILED):
            raise WorkflowLeaseExpiredError(
                aggregate_id=aggregate_id,
                lease_id=lease_id,
            )
        return record


# ============================================================================
# 5. Snapshot Manager (state rollback support)
# ============================================================================


def _snapshot_key(step_id: str, attempt: int) -> str:
    return f"{step_id}:{attempt}"


def _take_snapshot(state_data: Dict[str, Any]) -> str:
    """Return canonical JSON of state_data for rollback storage."""
    return canonical_json_text(state_data)


def _restore_snapshot(snapshot_json: str) -> Dict[str, Any]:
    """Restore state_data from a snapshot string."""
    return json.loads(snapshot_json)


# ============================================================================
# 6. Step Executor Protocol
# ============================================================================


class IStepExecutor(abc.ABC):
    """Protocol for executing a single pipeline step.

    Implementations are responsible for the actual side-effecting work.
    The WorkflowDispatcherRuntime calls execute() and interprets the result.
    """

    @abc.abstractmethod
    def execute(
        self,
        step_id: str,
        aggregate_id: str,
        state_data: Dict[str, Any],
        payload: Dict[str, Any],
        attempt: int,
    ) -> Dict[str, Any]:
        """Execute one step.

        Returns:
            A dict that will be stored as the step result.  Must not be None.

        Raises:
            Any exception signals a step failure; the dispatcher will handle
            retry / rollback logic according to the StepDefinition contract.
        """
        raise NotImplementedError


# ============================================================================
# 7. WorkflowDispatcherRuntime
# ============================================================================


class WorkflowDispatcherRuntime:
    """Orchestrates multi-stage program pipelines.

    Satisfies INV-DISP-002: no duplicate step execution; state consistency
    guaranteed across failures.

    Usage (happy path)::

        dispatcher = WorkflowDispatcherRuntime(store=store)
        run = dispatcher.initialize_pipeline(
            aggregate_id="prog-state:ws-1:my_program:run_abc",
            pipeline_id="my_pipeline_v1",
            actor_id="commander-1",
            actor_lane=AuthorityLane.COMMANDER,
            steps=[
                StepDefinition("ingest",   "Data Ingestion", max_attempts=3),
                StepDefinition("validate", "Schema Validation"),
                StepDefinition("emit",     "Emit Events", max_attempts=2),
            ],
        )
        for step_def in run.steps:
            run = dispatcher.execute_step(
                run=run,
                step_id=step_def.step_id,
                actor_id="commander-1",
                actor_lane=AuthorityLane.COMMANDER,
                payload={"key": "value"},
                executor=my_executor,
            )
        run = dispatcher.complete_pipeline(run, actor_id="commander-1",
                                           actor_lane=AuthorityLane.COMMANDER)

    The caller is responsible for iterating steps.  On failure,
    ``execute_step`` either retries (within max_attempts) or raises
    ``StepRetryLimitExceededError`` after rolling back the aggregate state.
    """

    def __init__(
        self,
        store: Optional[IProgramStateStore] = None,
        *,
        idempotency_registry: Optional[IdempotencyRegistry] = None,
        lease_manager: Optional[LeaseManager] = None,
    ) -> None:
        self._store = store or InMemoryProgramStateStore()
        self._idempotency = idempotency_registry or IdempotencyRegistry()
        self._lease_manager = lease_manager or LeaseManager()
        self._runs: Dict[str, PipelineRun] = {}
        self._run_lock = threading.RLock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def initialize_pipeline(
        self,
        *,
        aggregate_id: str,
        pipeline_id: str,
        actor_id: str,
        actor_lane: AuthorityLane,
        steps: Sequence[StepDefinition],
        run_id: Optional[str] = None,
    ) -> PipelineRun:
        """Initialise a new pipeline run and acquire the distributed lease.

        Preconditions:
          - Caller must be in COMMANDER lane.
          - The aggregate must exist in the store in RUNNING lifecycle.

        Returns:
            A PipelineRun in INITIALIZED status with the lease ACQUIRED.

        Raises:
            WorkflowAuthorityViolationError — non-COMMANDER caller.
            WorkflowAggregatePreconditionError — aggregate not RUNNING.
            WorkflowDispatchError — lease already held.
        """
        self._require_lane(actor_lane, AuthorityLane.COMMANDER, action="initialize_pipeline")
        aggregate = self._load_running_aggregate(aggregate_id)

        _run_id = run_id or _make_run_id(aggregate_id, pipeline_id)
        lease_id = _make_lease_id(_run_id)
        lease = self._lease_manager.acquire(
            aggregate_id=aggregate_id,
            pipeline_id=pipeline_id,
            actor_id=actor_id,
            lease_id=lease_id,
        )

        run = PipelineRun(
            run_id=_run_id,
            aggregate_id=aggregate_id,
            pipeline_id=pipeline_id,
            status=PipelineStatus.INITIALIZED,
            steps=list(steps),
            lease=lease,
        )
        with self._run_lock:
            self._runs[_run_id] = run

        logger.info(
            "pipeline_initialized run_id=%s aggregate_id=%s pipeline_id=%s steps=%d",
            _run_id, aggregate_id, pipeline_id, len(steps),
        )
        return run

    def execute_step(
        self,
        *,
        run: PipelineRun,
        step_id: str,
        actor_id: str,
        actor_lane: AuthorityLane,
        payload: Dict[str, Any],
        executor: IStepExecutor,
    ) -> PipelineRun:
        """Execute one pipeline step with idempotency, retry, and rollback.

        This is the core dispatch operation enforcing INV-DISP-002.

        Algorithm:
          1. Validate authority lane for the step.
          2. Compute idempotency key (pipeline_id + step_id + payload_sha).
          3. Check idempotency registry:
             - Key seen, same payload → SKIP (return immediately).
             - Key seen, different payload → CONFLICT error.
             - Key new → register and proceed.
          4. Advance lease to STEP_RUNNING.
          5. Take a pre-step snapshot of aggregate.state_data for rollback.
          6. Call executor.execute(…).
          7. On success: mark idempotency key complete, advance lease to
             STEP_COMPLETE, record StepExecutionRecord(COMPLETED).
          8. On failure: increment attempt counter:
             - attempt < max_attempts → update record(FAILED) and re-raise
               so the caller can retry.
             - attempt == max_attempts → rollback pre-step snapshot,
               update pipeline status to FAILED, release lease with FAILED
               status, raise StepRetryLimitExceededError.

        Returns:
            Updated PipelineRun (same object mutated in place; returned for
            composability).

        Raises:
            WorkflowAuthorityViolationError — caller lane insufficient.
            StepRetryLimitExceededError — max attempts exhausted; state rolled back.
            IdempotencyKeyConflictError — duplicate key with different payload.
            WorkflowStepNotFoundError — step_id not in pipeline.
        """
        step_def = run.step_by_id(step_id)
        self._require_lane(actor_lane, step_def.authority_lane, action=f"execute_step:{step_id}")

        attempt = run.attempt_count(step_id) + 1
        payload_sha = canonical_sha256(payload)
        idempotency_key = _make_step_idempotency_key(
            pipeline_id=run.pipeline_id,
            step_id=step_id,
            payload_sha=payload_sha,
        )

        # --- Idempotency check -------------------------------------------
        already_done, prior_record = self._idempotency.check_and_register(
            step_id=step_id,
            idempotency_key=idempotency_key,
            payload_sha=payload_sha,
        )
        if already_done:
            # Safe replay — skip without re-executing
            skip_rec = StepExecutionRecord(
                step_id=step_id,
                attempt=attempt,
                idempotency_key=idempotency_key,
                payload_sha=payload_sha,
                status=StepStatus.SKIPPED,
                completed_at=utc_now_rfc3339(),
                result=prior_record,  # carry forward prior result
            )
            run.records.append(skip_rec)
            logger.info(
                "step_skipped (idempotent) run_id=%s step_id=%s attempt=%d",
                run.run_id, step_id, attempt,
            )
            return run

        # --- Retry limit pre-check ----------------------------------------
        if attempt > step_def.max_attempts:
            raise StepRetryLimitExceededError(
                step_id=step_id,
                max_attempts=step_def.max_attempts,
                attempt=attempt,
            )

        # --- Advance lease -----------------------------------------------
        assert run.lease is not None, "Pipeline run must have an active lease"
        self._lease_manager.mark_step_running(
            aggregate_id=run.aggregate_id,
            lease_id=run.lease.lease_id,
            step_id=step_id,
        )

        # --- Snapshot current state_data (for rollback) ------------------
        aggregate = self._store.get_aggregate(run.aggregate_id)
        pre_state_json = _take_snapshot(aggregate.state_data if aggregate else {})
        snapshot_key = _snapshot_key(step_id, attempt)
        run.snapshots[snapshot_key] = pre_state_json

        # --- Record start ------------------------------------------------
        record = StepExecutionRecord(
            step_id=step_id,
            attempt=attempt,
            idempotency_key=idempotency_key,
            payload_sha=payload_sha,
            status=StepStatus.RUNNING,
            pre_snapshot_sha=canonical_sha256({"snapshot": pre_state_json}),
        )
        run.records.append(record)
        run.status = PipelineStatus.RUNNING

        # --- Execute ------------------------------------------------------
        try:
            result = executor.execute(
                step_id=step_id,
                aggregate_id=run.aggregate_id,
                state_data=_restore_snapshot(pre_state_json),
                payload=payload,
                attempt=attempt,
            )
        except Exception as exc:
            record.status = StepStatus.FAILED
            record.completed_at = utc_now_rfc3339()
            record.error_message = str(exc)

            if attempt >= step_def.max_attempts:
                # Exhausted — rollback and terminate the pipeline
                if step_def.rollback_on_failure:
                    self._rollback_step(run=run, step_id=step_id, attempt=attempt)
                run.status = PipelineStatus.FAILED
                run.completed_at = utc_now_rfc3339()
                self._lease_manager.fail(
                    aggregate_id=run.aggregate_id,
                    lease_id=run.lease.lease_id,
                    error_message=str(exc),
                )
                logger.error(
                    "step_retry_limit_exceeded run_id=%s step_id=%s attempt=%d/%d error=%s",
                    run.run_id, step_id, attempt, step_def.max_attempts, exc,
                )
                raise StepRetryLimitExceededError(
                    step_id=step_id,
                    max_attempts=step_def.max_attempts,
                    attempt=attempt,
                ) from exc
            else:
                # Still have attempts left — signal caller to retry
                logger.warning(
                    "step_attempt_failed run_id=%s step_id=%s attempt=%d/%d error=%s",
                    run.run_id, step_id, attempt, step_def.max_attempts, exc,
                )
                raise

        # --- Success path ------------------------------------------------
        record.status = StepStatus.COMPLETED
        record.completed_at = utc_now_rfc3339()
        record.result = result
        self._idempotency.mark_completed(
            idempotency_key=idempotency_key,
            completed_at=record.completed_at,
        )
        self._lease_manager.mark_step_complete(
            aggregate_id=run.aggregate_id,
            lease_id=run.lease.lease_id,
            step_id=step_id,
        )
        logger.info(
            "step_completed run_id=%s step_id=%s attempt=%d",
            run.run_id, step_id, attempt,
        )
        return run

    def complete_pipeline(
        self,
        run: PipelineRun,
        *,
        actor_id: str,
        actor_lane: AuthorityLane,
    ) -> PipelineRun:
        """Mark the pipeline as COMPLETED and release the distributed lease.

        Raises:
            WorkflowAuthorityViolationError — non-COMMANDER caller.
            WorkflowDispatchError — pipeline is not in RUNNING status.
        """
        self._require_lane(actor_lane, AuthorityLane.COMMANDER, action="complete_pipeline")
        if run.status not in (PipelineStatus.RUNNING, PipelineStatus.INITIALIZED):
            raise WorkflowDispatchError(
                f"Cannot complete pipeline '{run.run_id}': status is '{run.status.value}'",
                reason_code="PIPELINE_INVALID_TERMINAL_TRANSITION",
                details={"run_id": run.run_id, "current_status": run.status.value},
            )
        run.status = PipelineStatus.COMPLETED
        run.completed_at = utc_now_rfc3339()
        assert run.lease is not None
        self._lease_manager.release(
            aggregate_id=run.aggregate_id,
            lease_id=run.lease.lease_id,
        )
        logger.info("pipeline_completed run_id=%s", run.run_id)
        return run

    def get_pipeline_run(self, run_id: str) -> Optional[PipelineRun]:
        """Return a pipeline run by its run_id, or None if not found."""
        with self._run_lock:
            return self._runs.get(run_id)

    def get_lease_status(self, aggregate_id: str) -> Optional[LeaseStatus]:
        """Return the current lease status for an aggregate, or None."""
        record = self._lease_manager.get(aggregate_id)
        return record.status if record else None

    def heartbeat(self, run: PipelineRun) -> None:
        """Send a lease heartbeat to signal continued ownership."""
        assert run.lease is not None
        self._lease_manager.heartbeat(
            aggregate_id=run.aggregate_id,
            lease_id=run.lease.lease_id,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _require_lane(
        self,
        actor_lane: AuthorityLane,
        required_lane: AuthorityLane,
        *,
        action: str,
    ) -> None:
        """Fail closed if the caller's lane is below the required minimum."""
        _LANE_RANK = {
            AuthorityLane.HUNTER: 0,
            AuthorityLane.ANALYST: 1,
            AuthorityLane.COMPOSER: 2,
            AuthorityLane.COMMANDER: 3,
        }
        if _LANE_RANK[actor_lane] < _LANE_RANK[required_lane]:
            raise WorkflowAuthorityViolationError(
                action=action,
                actor_lane=actor_lane,
                required_lane=required_lane,
            )

    def _load_running_aggregate(self, aggregate_id: str) -> ProgramStateAggregate:
        """Load aggregate and verify it is in RUNNING lifecycle."""
        aggregate = self._store.get_aggregate(aggregate_id)
        if aggregate is None:
            raise WorkflowDispatchError(
                f"Aggregate '{aggregate_id}' not found in store",
                reason_code="AGGREGATE_NOT_FOUND",
                details={"aggregate_id": aggregate_id},
            )
        if aggregate.lifecycle != ProgramStateLifecycle.RUNNING:
            raise WorkflowAggregatePreconditionError(
                aggregate_id=aggregate_id,
                required=ProgramStateLifecycle.RUNNING.value,
                actual=aggregate.lifecycle.value,
            )
        return aggregate

    def _rollback_step(
        self,
        run: PipelineRun,
        step_id: str,
        attempt: int,
    ) -> None:
        """Restore aggregate state_data to the pre-step snapshot.

        Mutates the stored aggregate's state_data via the store's
        save_aggregate method using the snapshot captured before the step ran.

        Raises:
            WorkflowRollbackError — if no snapshot is available or the
                aggregate cannot be found.
        """
        snapshot_key = _snapshot_key(step_id, attempt)
        snapshot_json = run.snapshots.get(snapshot_key)
        if snapshot_json is None:
            raise WorkflowRollbackError(
                aggregate_id=run.aggregate_id,
                step_id=step_id,
                reason=f"No pre-step snapshot found for key '{snapshot_key}'",
            )
        restored_data = _restore_snapshot(snapshot_json)
        aggregate = self._store.get_aggregate(run.aggregate_id)
        if aggregate is None:
            raise WorkflowRollbackError(
                aggregate_id=run.aggregate_id,
                step_id=step_id,
                reason="Aggregate not found during rollback",
            )

        # Build a rolled-back aggregate preserving identity fields
        rolled_back = ProgramStateAggregate(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state=aggregate.current_state,
            state_data=restored_data,
            version=aggregate.version,
            state_hash=aggregate.state_hash,
            lifecycle=aggregate.lifecycle,
            last_receipt_id=aggregate.last_receipt_id,
            created_at=aggregate.created_at,
            updated_at=utc_now_rfc3339(),
        )
        self._store.save_aggregate(rolled_back)

        # Mark the step records as ROLLED_BACK
        for rec in run.records:
            if rec.step_id == step_id and rec.status == StepStatus.FAILED:
                rec.status = StepStatus.ROLLED_BACK

        logger.info(
            "step_rolled_back run_id=%s step_id=%s attempt=%d snapshot_key=%s",
            run.run_id, step_id, attempt, snapshot_key,
        )


# ============================================================================
# 8. Factory / convenience helpers
# ============================================================================


def _make_run_id(aggregate_id: str, pipeline_id: str) -> str:
    raw = f"dispatch:{aggregate_id}:{pipeline_id}:{utc_now_rfc3339()}"
    return "run_" + hashlib.sha256(raw.encode()).hexdigest()[:24]


def _make_lease_id(run_id: str) -> str:
    return "lease_" + hashlib.sha256(f"lease:{run_id}".encode()).hexdigest()[:24]


def _make_step_idempotency_key(
    pipeline_id: str,
    step_id: str,
    payload_sha: str,
) -> str:
    """Derive a deterministic idempotency key from pipeline + step + payload.

    INV-DISP-002: the key must be stable across process restarts for the
    same logical operation, so we do NOT include timestamps.
    """
    return canonical_sha256({
        "pipeline_id": pipeline_id,
        "step_id": step_id,
        "payload_sha": payload_sha,
    })


def create_workflow_dispatcher(
    store: Optional[IProgramStateStore] = None,
) -> WorkflowDispatcherRuntime:
    """Factory: create a WorkflowDispatcherRuntime with default collaborators."""
    return WorkflowDispatcherRuntime(
        store=store or InMemoryProgramStateStore(),
        idempotency_registry=IdempotencyRegistry(),
        lease_manager=LeaseManager(),
    )
