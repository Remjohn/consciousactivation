from __future__ import annotations

from .application import AirApplication


def status() -> dict[str, object]:
    return AirApplication().status()
