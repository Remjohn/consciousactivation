from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping

from cmf_builder.application.productization_contracts import (
    ProductizationCommandResult,
    ProductizationError,
)


def render_result(
    result: ProductizationCommandResult, *, output_format: str
) -> str:
    payload = {
        "artifact_hash": result.artifact_hash,
        "artifact_id": result.artifact_id,
        "command": result.command,
        "payload": result.payload,
        "receipt_id": result.receipt_id,
        "status": result.status,
    }
    if output_format == "json":
        return canonical_json(payload)
    if output_format == "human":
        return _human_result(payload)
    raise ValueError(f"unsupported output format: {output_format}")


def render_productization_error(
    error: ProductizationError, *, output_format: str
) -> str:
    payload = {
        "error": {
            "code": error.code.value,
            "context": error.context,
            "field_path": error.field_path,
            "message": str(error),
        },
        "status": "ERROR",
    }
    if output_format == "json":
        return canonical_json(payload)
    if output_format == "human":
        return _human_error(payload)
    raise ValueError(f"unsupported output format: {output_format}")


def render_usage_error(message: str, *, output_format: str) -> str:
    payload = {
        "error": {
            "code": "CLI_USAGE",
            "context": {},
            "field_path": None,
            "message": message,
        },
        "status": "ERROR",
    }
    if output_format == "json":
        return canonical_json(payload)
    return _human_error(payload)


def render_internal_error(*, output_format: str) -> str:
    payload = {
        "error": {
            "code": "INTERNAL_ERROR",
            "context": {},
            "field_path": None,
            "message": "The Builder command failed unexpectedly.",
        },
        "status": "ERROR",
    }
    if output_format == "json":
        return canonical_json(payload)
    return _human_error(payload)


def canonical_json(value: object) -> str:
    normalized = _normalize_json(value)
    return (
        json.dumps(
            normalized,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    )


def _normalize_json(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return _normalize_json(value.value)
    if isinstance(value, Path):
        return value.as_posix()
    if is_dataclass(value) and not isinstance(value, type):
        return _normalize_json(asdict(value))
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("CLI JSON mappings require string keys")
            normalized[key] = _normalize_json(item)
        return normalized
    if isinstance(value, (tuple, list)):
        return [_normalize_json(item) for item in value]
    raise TypeError(f"unsupported CLI output value: {type(value).__name__}")


def _human_result(payload: Mapping[str, object]) -> str:
    lines = [
        f"command: {_human_value(payload['command'])}",
        f"status: {_human_value(payload['status'])}",
        f"artifact_id: {_human_value(payload['artifact_id'])}",
        f"artifact_hash: {_human_value(payload['artifact_hash'])}",
        f"receipt_id: {_human_value(payload['receipt_id'])}",
    ]
    result_payload = payload["payload"]
    if not isinstance(result_payload, Mapping):
        raise TypeError("ProductizationCommandResult.payload must be a mapping")
    for key in sorted(result_payload):
        if not isinstance(key, str):
            raise TypeError("CLI human-output mappings require string keys")
        lines.append(f"payload.{key}: {_human_value(result_payload[key])}")
    return "\n".join(lines) + "\n"


def _human_error(payload: Mapping[str, object]) -> str:
    error = payload["error"]
    if not isinstance(error, Mapping):
        raise TypeError("CLI error payload must be a mapping")
    lines = [
        f"status: {_human_value(payload['status'])}",
        f"error_code: {_human_value(error['code'])}",
        f"message: {_human_value(error['message'])}",
    ]
    if error["field_path"] is not None:
        lines.append(f"field_path: {_human_value(error['field_path'])}")
    context = error["context"]
    if not isinstance(context, Mapping):
        raise TypeError("CLI error context must be a mapping")
    for key in sorted(context):
        if not isinstance(key, str):
            raise TypeError("CLI error-context mappings require string keys")
        lines.append(f"context.{key}: {_human_value(context[key])}")
    return "\n".join(lines) + "\n"


def _human_value(value: object) -> str:
    return canonical_json(value).rstrip("\n")
