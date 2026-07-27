from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath
from typing import Any, Iterable

from ca_contracts import canonical_sha256

from .errors import PipelineValidationError

_SHA = re.compile(r"^[0-9a-f]{64}$")
_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_DRIVE = re.compile(r"^[A-Za-z]:[\\/]")


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PipelineValidationError(f"{field} must be a non-empty string")
    return value.strip()


def require_int(value: Any, field: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise PipelineValidationError(f"{field} must be an integer >= {minimum}")
    return value


def require_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise PipelineValidationError(f"{field} must be a boolean")
    return value


def require_sha(value: Any, field: str) -> str:
    text = require_string(value, field).removeprefix("sha256:")
    if not _SHA.fullmatch(text):
        raise PipelineValidationError(f"{field} must be a lowercase SHA-256")
    return text


def require_semver(value: Any, field: str) -> str:
    text = require_string(value, field)
    if not _SEMVER.fullmatch(text):
        raise PipelineValidationError(f"{field} must be a semantic version")
    return text


def require_relative_path(value: Any, field: str) -> str:
    text = require_string(value, field).replace("\\", "/")
    if text.startswith("/") or text.startswith("//") or _DRIVE.match(text) or "\x00" in text:
        raise PipelineValidationError(f"{field} must be a portable relative path")
    parts = PurePosixPath(text).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise PipelineValidationError(f"{field} contains an unsafe path component")
    return str(PurePosixPath(*parts))


def require_ref(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise PipelineValidationError(f"{field} must be an immutable reference")
    allowed = {"object_id", "version", "sha256"}
    if set(value) != allowed:
        raise PipelineValidationError(f"{field} must contain exactly {sorted(allowed)}")
    return {
        "object_id": require_string(value["object_id"], f"{field}.object_id"),
        "version": require_semver(value["version"], f"{field}.version"),
        "sha256": require_sha(value["sha256"], f"{field}.sha256"),
    }


def require_authority(value: Any, field: str = "authority") -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise PipelineValidationError(f"{field} must be an authority reference")
    allowed = {"authority_id", "authority_version", "authority_sha256", "authority_state"}
    if set(value) != allowed:
        raise PipelineValidationError(f"{field} must contain exactly {sorted(allowed)}")
    return {
        "authority_id": require_string(value["authority_id"], f"{field}.authority_id"),
        "authority_version": require_string(value["authority_version"], f"{field}.authority_version"),
        "authority_sha256": require_sha(value["authority_sha256"], f"{field}.authority_sha256"),
        "authority_state": require_string(value["authority_state"], f"{field}.authority_state"),
    }


def require_string_list(value: Any, field: str, *, non_empty: bool = False, sorted_unique: bool = True) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        suffix = " and non-empty" if non_empty else ""
        raise PipelineValidationError(f"{field} must be a list{suffix}")
    items = [require_string(item, f"{field}[{index}]") for index, item in enumerate(value)]
    if len(items) != len(set(items)):
        raise PipelineValidationError(f"{field} must not contain duplicates")
    if sorted_unique and items != sorted(items):
        raise PipelineValidationError(f"{field} must be lexicographically sorted")
    return items


def require_ref_list(value: Any, field: str, *, non_empty: bool = False, sorted_by_id: bool = True) -> list[dict[str, str]]:
    if not isinstance(value, list) or (non_empty and not value):
        suffix = " and non-empty" if non_empty else ""
        raise PipelineValidationError(f"{field} must be a list{suffix}")
    items = [require_ref(item, f"{field}[{index}]") for index, item in enumerate(value)]
    ids = [item["object_id"] for item in items]
    if len(ids) != len(set(ids)):
        raise PipelineValidationError(f"{field} must not contain duplicate object IDs")
    if sorted_by_id and ids != sorted(ids):
        raise PipelineValidationError(f"{field} must be sorted by object_id")
    return items


def reject_unknown(payload: Mapping[str, Any], allowed: Iterable[str], label: str) -> None:
    unknown = sorted(set(payload) - set(allowed))
    if unknown:
        raise PipelineValidationError(f"{label} contains unknown governed fields: {unknown}")


def reject_noncanonical(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise PipelineValidationError(f"{path}: floating-point values are forbidden")
    if isinstance(value, str):
        if _DRIVE.match(value) or value.startswith("file:///") or value.startswith("/home/") or value.startswith("/tmp/"):
            raise PipelineValidationError(f"{path}: host path leakage is forbidden")
        return
    if value is None or isinstance(value, (int, bool)):
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise PipelineValidationError(f"{path}: object keys must be non-empty strings")
            reject_noncanonical(item, f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            reject_noncanonical(item, f"{path}[{index}]")
        return
    raise PipelineValidationError(f"{path}: unsupported canonical value {type(value).__name__}")


def semantic_identity(prefix: str, payload: Mapping[str, Any]) -> str:
    reject_noncanonical(payload)
    return f"{prefix}:{canonical_sha256(payload)}"


def immutable_ref(object_id: str, version: str, payload: Mapping[str, Any]) -> dict[str, str]:
    return {"object_id": object_id, "version": require_semver(version, "version"), "sha256": canonical_sha256(payload)}
