"""Atomic in-memory persistence adapter for tests and the reference slice."""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from threading import RLock
from typing import Iterator

from .errors import PersistenceError
from .models import (
    CorrelationRecord,
    DelegationSetRecord,
    IdempotencyRecord,
    OutboxEntry,
    ReplayRecord,
    StoredDecision,
)


class InMemoryProtocolStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._correlations: dict[str, CorrelationRecord] = {}
        self._messages: dict[str, StoredDecision] = {}
        self._nonces: dict[tuple[str, str, str], ReplayRecord] = {}
        self._idempotency: dict[tuple[str, str, str, str], IdempotencyRecord] = {}
        self._sets: dict[str, DelegationSetRecord] = {}
        self._outbox: list[OutboxEntry] = []
        self._fail_next_commit: str | None = None

    @contextmanager
    def locked(self) -> Iterator[None]:
        with self._lock:
            yield

    def correlation_copy(self, correlation_id: str) -> CorrelationRecord:
        return deepcopy(
            self._correlations.get(
                correlation_id,
                CorrelationRecord(correlation_id=correlation_id),
            )
        )

    def message(self, message_id: str) -> StoredDecision | None:
        return self._messages.get(message_id)

    def nonce(self, key: tuple[str, str, str]) -> ReplayRecord | None:
        return self._nonces.get(key)

    def idempotency(self, key: tuple[str, str, str, str]) -> IdempotencyRecord | None:
        return self._idempotency.get(key)

    def fail_next_commit(self, reason: str = "injected failure") -> None:
        self._fail_next_commit = reason

    def pin_compatibility(self, correlation_id: str, profile: dict[str, object]) -> None:
        with self._lock:
            record = self.correlation_copy(correlation_id)
            if record.compatibility_profile is not None and record.compatibility_profile != profile:
                raise ValueError("Compatibility profile is already pinned for this correlation")
            record.compatibility_profile = deepcopy(profile)
            self._correlations[correlation_id] = record

    def commit(
        self,
        *,
        correlation: CorrelationRecord,
        message_id: str,
        stored_decision: StoredDecision,
        nonce_key: tuple[str, str, str] | None,
        replay_record: ReplayRecord | None,
        idempotency_key: tuple[str, str, str, str] | None,
        idempotency_record: IdempotencyRecord | None,
        outbox_entry: OutboxEntry,
        delegation_set: DelegationSetRecord | None = None,
        preserve_existing_message: bool = False,
        preserve_existing_nonce: bool = False,
    ) -> None:
        if self._fail_next_commit is not None:
            reason = self._fail_next_commit
            self._fail_next_commit = None
            raise PersistenceError(reason)
        self._correlations[correlation.correlation_id] = deepcopy(correlation)
        if not preserve_existing_message:
            self._messages[message_id] = stored_decision
        if nonce_key is not None and replay_record is not None and not preserve_existing_nonce:
            self._nonces[nonce_key] = replay_record
        if idempotency_key is not None and idempotency_record is not None:
            self._idempotency[idempotency_key] = idempotency_record
        if delegation_set is not None:
            self._sets[delegation_set.set_id] = delegation_set
        self._outbox.append(outbox_entry)

    def next_outbox_sequence(self) -> int:
        return len(self._outbox) + 1

    def state(self, correlation_id: str) -> str:
        return self.correlation_copy(correlation_id).state

    def audit(self, correlation_id: str):
        return tuple(self.correlation_copy(correlation_id).audit)

    def outbox(self) -> tuple[OutboxEntry, ...]:
        return tuple(deepcopy(self._outbox))

    def delegation_set(self, set_id: str) -> DelegationSetRecord | None:
        return deepcopy(self._sets.get(set_id))

    def snapshot(self) -> dict[str, object]:
        return deepcopy(
            {
                "correlations": self._correlations,
                "messages": self._messages,
                "nonces": self._nonces,
                "idempotency": self._idempotency,
                "sets": self._sets,
                "outbox": self._outbox,
            }
        )
