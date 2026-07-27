from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath
from typing import Any

from ca_contracts import canonical_sha256

from .errors import VAEValidationError

_SHA = re.compile(r"^[0-9a-f]{64}$")
_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_DRIVE = re.compile(r"^[A-Za-z]:[\\/]")


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VAEValidationError(f"{field} must be a non-empty string")
    return value.strip()


def require_int(value: Any, field: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise VAEValidationError(f"{field} must be an integer >= {minimum}")
    return value


def require_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise VAEValidationError(f"{field} must be a boolean")
    return value


def require_sha(value: Any, field: str) -> str:
    text = require_string(value, field).removeprefix("sha256:")
    if not _SHA.fullmatch(text):
        raise VAEValidationError(f"{field} must be a lowercase SHA-256")
    return text


def require_semver(value: Any, field: str) -> str:
    text = require_string(value, field)
    if not _SEMVER.fullmatch(text):
        raise VAEValidationError(f"{field} must be a semantic version")
    return text


def require_ref(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != {"object_id", "version", "sha256"}:
        raise VAEValidationError(f"{field} must be an immutable object reference")
    return {
        "object_id": require_string(value["object_id"], f"{field}.object_id"),
        "version": require_semver(value["version"], f"{field}.version"),
        "sha256": require_sha(value["sha256"], f"{field}.sha256"),
    }


def require_resource_ref(value: Any, field: str) -> dict[str, str]:
    required = {"resource_id", "version", "payload_hash", "canonical_ref"}
    if not isinstance(value, Mapping) or set(value) != required:
        raise VAEValidationError(f"{field} must be a Delegation ResourceIdentityRef")
    canonical = require_string(value["canonical_ref"], f"{field}.canonical_ref")
    if not canonical.startswith("cmf-contract://"):
        raise VAEValidationError(f"{field}.canonical_ref must use cmf-contract://")
    return {
        "resource_id": require_string(value["resource_id"], f"{field}.resource_id"),
        "version": require_string(value["version"], f"{field}.version"),
        "payload_hash": "sha256:" + require_sha(value["payload_hash"], f"{field}.payload_hash"),
        "canonical_ref": canonical,
    }


def safe_relative(value: Any, field: str) -> str:
    text = require_string(value, field).replace("\\", "/")
    if text.startswith("/") or text.startswith("//") or _DRIVE.match(text):
        raise VAEValidationError(f"{field} must be a portable relative path")
    parts = PurePosixPath(text).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise VAEValidationError(f"{field} contains unsafe path components")
    return str(PurePosixPath(*parts))


def reject_noncanonical(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise VAEValidationError(f"{path}: floating point is forbidden in canonical records")
    if isinstance(value, str):
        if _DRIVE.match(value) or value.startswith("file:///") or value.startswith("/tmp/") or value.startswith("/home/"):
            raise VAEValidationError(f"{path}: host path leakage is forbidden")
        return
    if value is None or isinstance(value, (int, bool)):
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise VAEValidationError(f"{path}: object keys must be non-empty strings")
            reject_noncanonical(item, f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            reject_noncanonical(item, f"{path}[{index}]")
        return
    raise VAEValidationError(f"{path}: unsupported canonical value {type(value).__name__}")


def semantic_id(prefix: str, payload: Mapping[str, Any]) -> str:
    reject_noncanonical(payload)
    return f"{prefix}:{canonical_sha256(payload)}"
