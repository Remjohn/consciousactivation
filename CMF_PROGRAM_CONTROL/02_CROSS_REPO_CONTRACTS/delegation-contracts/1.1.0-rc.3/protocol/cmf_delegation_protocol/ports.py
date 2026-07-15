"""Transport- and infrastructure-neutral protocol ports."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...


class SignatureVerifier(Protocol):
    def verify(self, envelope: dict[str, Any], payload: Any) -> bool: ...

