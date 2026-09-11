from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from ca_contracts import canonical_sha256

from .errors import ValidationError

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
PORTABLE_URI_PREFIXES = ("workspace://", "source://", "artifact://", "memory://")


def exact_keys(value: Mapping[str, Any], required: set[str], name: str) -> None:
    observed = set(value)
    if observed != required:
        raise ValidationError(f"{name} fields mismatch", context={"required": sorted(required), "observed": sorted(observed)})


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    return value.strip()


def require_int(value: Any, name: str, *, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{name} must be an integer")
    if minimum is not None and value < minimum:
        raise ValidationError(f"{name} must be >= {minimum}")
    return value


def require_sha(value: Any, name: str) -> str:
    text = require_string(value, name)
    if not SHA_RE.fullmatch(text):
        raise ValidationError(f"{name} must be a lowercase SHA-256")
    return text


def require_enum(value: Any, allowed: set[str], name: str) -> str:
    text = require_string(value, name)
    if text not in allowed:
        raise ValidationError(f"{name} must be one of {sorted(allowed)}")
    return text


def require_ref(value: Any, name: str = "ref") -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{name} must be an object")
    exact_keys(value, {"object_id", "version", "sha256"}, name)
    return {
        "object_id": require_string(value["object_id"], f"{name}.object_id"),
        "version": require_string(value["version"], f"{name}.version"),
        "sha256": require_sha(value["sha256"], f"{name}.sha256"),
    }


def require_source_span(value: Any, name: str = "source_span") -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{name} must be an object")
    required = {"source_id", "source_version", "source_sha256", "start_ms", "end_ms", "speaker_id"}
    exact_keys(value, required, name)
    start = require_int(value["start_ms"], f"{name}.start_ms", minimum=0)
    end = require_int(value["end_ms"], f"{name}.end_ms", minimum=1)
    if end <= start:
        raise ValidationError(f"{name}.end_ms must be greater than start_ms")
    return {
        "source_id": require_string(value["source_id"], f"{name}.source_id"),
        "source_version": require_string(value["source_version"], f"{name}.source_version"),
        "source_sha256": require_sha(value["source_sha256"], f"{name}.source_sha256"),
        "start_ms": start,
        "end_ms": end,
        "speaker_id": require_string(value["speaker_id"], f"{name}.speaker_id"),
    }


def require_portable_uri(value: Any, name: str = "logical_uri") -> str:
    uri = require_string(value, name)
    if not uri.startswith(PORTABLE_URI_PREFIXES):
        raise ValidationError(f"{name} must use a governed portable URI scheme")
    if ".." in uri or "\\" in uri or re.match(r"^[A-Za-z]:", uri):
        raise ValidationError(f"{name} contains a non-portable path")
    return uri


def semantic_id(prefix: str, payload: Mapping[str, Any]) -> str:
    return f"{prefix}:{canonical_sha256(dict(payload))[:32]}"


def immutable_ref(object_id: str, payload: Mapping[str, Any], *, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": canonical_sha256(dict(payload))}


def sorted_unique_strings(value: Any, name: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValidationError(f"{name} must be a list")
    result = [require_string(item, f"{name}[]") for item in value]
    if len(result) != len(set(result)):
        raise ValidationError(f"{name} contains duplicates")
    return sorted(result)
