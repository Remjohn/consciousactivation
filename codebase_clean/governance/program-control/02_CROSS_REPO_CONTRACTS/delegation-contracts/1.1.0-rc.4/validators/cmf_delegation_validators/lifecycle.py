"""Deterministic delegation lifecycle transition validation."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Iterable

from .paths import CONTRACTS_ROOT


class LifecycleError(ValueError):
    """Raised when an event cannot legally advance the lifecycle."""


@lru_cache(maxsize=1)
def load_lifecycle() -> dict[str, Any]:
    return json.loads((CONTRACTS_ROOT / "lifecycle.json").read_text(encoding="utf-8"))


def transition(current_state: str, trigger: str, principal_type: str) -> str:
    matches = [
        item
        for item in load_lifecycle()["transitions"]
        if item["from_state"] == current_state
        and item["trigger"] == trigger
        and item["principal_type"] == principal_type
    ]
    if len(matches) != 1:
        raise LifecycleError(
            f"Illegal or ambiguous transition: {current_state} + {trigger} by {principal_type}"
        )
    return matches[0]["to_state"]


def validate_sequence(sequence: Iterable[dict[str, Any]]) -> str:
    current: str | None = None
    for index, item in enumerate(sequence):
        if index == 0:
            current = item["from_state"]
        if item["from_state"] != current:
            raise LifecycleError(
                f"Non-contiguous lifecycle sequence: expected {current}, got {item['from_state']}"
            )
        actual = transition(current, item["trigger"], item["principal_type"])
        if actual != item["to_state"]:
            raise LifecycleError(f"Expected {item['to_state']}, transition resolves to {actual}")
        current = actual
    if current is None:
        raise LifecycleError("Lifecycle sequence may not be empty")
    return current

