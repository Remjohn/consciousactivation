"""RFC 8785 canonical JSON for the protocol's safe-integer JSON profile."""

from __future__ import annotations

import hashlib
import json
from typing import Any


MAX_SAFE_INTEGER = 9_007_199_254_740_991


class CanonicalizationError(ValueError):
    """Raised when a value is outside the canonical protocol profile."""


def _string(value: str) -> str:
    try:
        value.encode("utf-16", "strict")
    except UnicodeEncodeError as exc:
        raise CanonicalizationError("Lone Unicode surrogates are not canonical JSON") from exc
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _sort_key(value: str) -> bytes:
    try:
        return value.encode("utf-16-be", "strict")
    except UnicodeEncodeError as exc:
        raise CanonicalizationError("Object keys may not contain lone Unicode surrogates") from exc


def _serialize(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise CanonicalizationError("Integers must remain inside the IEEE-754 safe range")
        return str(value)
    if isinstance(value, float):
        raise CanonicalizationError(
            "Floating-point values are forbidden; use integers, basis points, minor units, or strings"
        )
    if isinstance(value, str):
        return _string(value)
    if isinstance(value, list):
        return "[" + ",".join(_serialize(item) for item in value) + "]"
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise CanonicalizationError("Canonical JSON object keys must be strings")
        parts = [
            _string(key) + ":" + _serialize(value[key])
            for key in sorted(value, key=_sort_key)
        ]
        return "{" + ",".join(parts) + "}"
    raise CanonicalizationError(f"Unsupported canonical JSON value: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    """Return RFC 8785-compatible bytes for the protocol's no-float profile."""

    return _serialize(value).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()

