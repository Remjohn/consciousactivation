"""Clock implementations used by the transport-neutral protocol engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass
class FrozenClock:
    instant: datetime

    def now(self) -> datetime:
        return self.instant

