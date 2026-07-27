"""Typed failures emitted by the local reference protocol."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProtocolRejection(Exception):
    code: str
    stage: str
    detail: str
    retryable: bool = False

    def __str__(self) -> str:
        return f"{self.code} at {self.stage}: {self.detail}"


class PersistenceError(RuntimeError):
    """Raised by the test persistence adapter before an atomic commit."""

