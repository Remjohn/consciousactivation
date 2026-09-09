"""Authoritative operator preemption controls for CA-M046 / INV-PREEMPT-001.

The module deliberately separates three concerns:

* ``ExecutionCancellationToken`` is the in-memory execution lock/preemption signal.
* ``ExecutionControlRegistry`` binds one token to one canonical execution aggregate.
* ``PreemptionReceipt`` records the accepted operator request and interruption outcome.

State remains authoritative in ``UniversalProgramStateRuntime``; this module never
writes program state or invents lifecycle states.  It only coordinates interruption
of the active execution boundary and supplies durable receipt material to the caller.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Tuple

from ca_contracts import canonical_sha256


class ExecutionPreemptionError(RuntimeError):
    """Base class for execution-preemption violations."""


class ExecutionCancelledError(ExecutionPreemptionError):
    """Raised by a real worker boundary after operator cancellation is observed."""

    def __init__(self, aggregate_id: str, *, reason: str = "operator abort") -> None:
        super().__init__(f"Execution '{aggregate_id}' cancelled: {reason}")
        self.aggregate_id = aggregate_id
        self.reason = reason


@dataclass(frozen=True, slots=True)
class CancellationCallbackFailure:
    """Failure observed while propagating cancellation to one bound resource."""

    resource: str
    message: str


@dataclass(frozen=True, slots=True)
class CancellationObservation:
    """Immutable result of a cancellation signal propagation attempt."""

    aggregate_id: str
    requested_at: str
    observed_at: str
    latency_ms: float
    already_cancelled: bool
    resources_notified: Tuple[str, ...] = ()
    callback_failures: Tuple[CancellationCallbackFailure, ...] = ()

    @property
    def observed(self) -> bool:
        """Whether the token is in the cancelled state at the observation point."""
        return True


@dataclass(frozen=True, slots=True)
class PreemptionReceipt:
    """Receipt material for an accepted operator abort transition."""

    receipt_id: str
    aggregate_id: str
    workspace_id: str
    actor_id: str
    source_state: str
    target_state: str
    expected_version: Optional[int]
    committed_version: int
    cancellation_requested_at: str
    cancellation_observed_at: Optional[str]
    cancellation_latency_ms: Optional[float]
    cancellation_observed: bool
    resources_notified: Tuple[str, ...] = ()
    callback_failures: Tuple[CancellationCallbackFailure, ...] = ()
    reason: str = "operator abort"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    receipt_sha256: str = ""

    def __post_init__(self) -> None:
        if self.receipt_sha256:
            return
        material = self.canonical_dict(include_digest=False)
        object.__setattr__(self, "receipt_sha256", canonical_sha256(material))

    def canonical_dict(self, *, include_digest: bool = True) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "receipt_id": self.receipt_id,
            "aggregate_id": self.aggregate_id,
            "workspace_id": self.workspace_id,
            "actor_id": self.actor_id,
            "source_state": self.source_state,
            "target_state": self.target_state,
            "expected_version": self.expected_version,
            "committed_version": self.committed_version,
            "cancellation_requested_at": self.cancellation_requested_at,
            "cancellation_observed_at": self.cancellation_observed_at,
            "cancellation_latency_ms": self.cancellation_latency_ms,
            "cancellation_observed": self.cancellation_observed,
            "resources_notified": list(self.resources_notified),
            "callback_failures": [
                {"resource": failure.resource, "message": failure.message}
                for failure in self.callback_failures
            ],
            "reason": self.reason,
            "created_at": self.created_at,
        }
        if include_digest:
            payload["receipt_sha256"] = self.receipt_sha256
        return payload


CancellationCallback = Callable[[], None]


class ExecutionCancellationToken:
    """Thread-safe cancellation signal shared by a live execution boundary."""

    def __init__(self, aggregate_id: str) -> None:
        self.aggregate_id = aggregate_id
        self._event = threading.Event()
        self._lock = threading.RLock()
        self._callbacks: Dict[str, CancellationCallback] = {}
        self._requested_at: Optional[str] = None
        self._observed_at: Optional[str] = None
        self._callback_failures: List[CancellationCallbackFailure] = []

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    @property
    def requested_at(self) -> Optional[str]:
        with self._lock:
            return self._requested_at

    @property
    def observed_at(self) -> Optional[str]:
        with self._lock:
            return self._observed_at

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Block until cancellation is requested, returning the Event result."""
        return self._event.wait(timeout)

    def raise_if_cancelled(self) -> None:
        """Fail fast at a safe worker boundary when the operator signal is set."""
        if self._event.is_set():
            with self._lock:
                if self._observed_at is None:
                    self._observed_at = _utc_now()
            raise ExecutionCancelledError(self.aggregate_id)

    def add_callback(self, resource: str, callback: CancellationCallback) -> None:
        """Bind a cancellation callback such as a socket/tool/worker shutdown hook."""
        if not resource or not resource.strip():
            raise ValueError("resource must be a non-empty string")
        if not callable(callback):
            raise TypeError("callback must be callable")
        with self._lock:
            if self._event.is_set():
                callback()
                return
            self._callbacks[resource] = callback

    def cancel(self) -> CancellationObservation:
        """Set the signal and synchronously notify every currently bound resource."""
        started = time.monotonic()
        requested_at = _utc_now()
        with self._lock:
            already_cancelled = self._event.is_set()
            if not already_cancelled:
                self._requested_at = requested_at
                self._event.set()
            else:
                requested_at = self._requested_at or requested_at
            callbacks = list(self._callbacks.items())

        failures: List[CancellationCallbackFailure] = []
        resources_notified: List[str] = []
        for resource, callback in callbacks:
            try:
                callback()
                resources_notified.append(resource)
            except Exception as exc:  # cancellation evidence must retain propagation failures
                failure = CancellationCallbackFailure(resource=resource, message=str(exc)[:500])
                failures.append(failure)
                with self._lock:
                    self._callback_failures.append(failure)

        observed_at = _utc_now()
        with self._lock:
            self._observed_at = observed_at
            self._callback_failures.extend(failure for failure in failures if failure not in self._callback_failures)

        return CancellationObservation(
            aggregate_id=self.aggregate_id,
            requested_at=requested_at,
            observed_at=observed_at,
            latency_ms=(time.monotonic() - started) * 1000.0,
            already_cancelled=already_cancelled,
            resources_notified=tuple(resources_notified),
            callback_failures=tuple(failures),
        )

    def callback_failures(self) -> Tuple[CancellationCallbackFailure, ...]:
        with self._lock:
            return tuple(self._callback_failures)


class ExecutionControlRegistry:
    """Thread-safe mapping from canonical aggregate IDs to live cancellation tokens."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._tokens: Dict[str, ExecutionCancellationToken] = {}

    def bind(self, aggregate_id: str) -> ExecutionCancellationToken:
        if not aggregate_id:
            raise ValueError("aggregate_id must be non-empty")
        with self._lock:
            token = self._tokens.get(aggregate_id)
            if token is None:
                token = ExecutionCancellationToken(aggregate_id)
                self._tokens[aggregate_id] = token
            return token

    def get(self, aggregate_id: str) -> Optional[ExecutionCancellationToken]:
        with self._lock:
            return self._tokens.get(aggregate_id)

    def unbind(self, aggregate_id: str) -> Optional[ExecutionCancellationToken]:
        with self._lock:
            return self._tokens.pop(aggregate_id, None)

    def cancel(self, aggregate_id: str) -> CancellationObservation:
        token = self.get(aggregate_id)
        if token is None:
            token = self.bind(aggregate_id)
        return token.cancel()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


__all__ = [
    "CancellationCallbackFailure",
    "CancellationObservation",
    "ExecutionCancelledError",
    "ExecutionCancellationToken",
    "ExecutionControlRegistry",
    "ExecutionPreemptionError",
    "PreemptionReceipt",
]
