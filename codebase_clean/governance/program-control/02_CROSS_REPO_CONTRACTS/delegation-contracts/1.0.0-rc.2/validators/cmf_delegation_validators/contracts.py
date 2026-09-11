"""Schema, registry, and example validation."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator, FormatChecker

from .paths import CONTRACTS_ROOT, ROOT


class ContractError(ValueError):
    """Raised when contract metadata or payload validation fails."""


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    return _read_json(CONTRACTS_ROOT / "registry.json")


def registry_entry(message_type: str) -> dict[str, Any]:
    matches = [item for item in load_registry()["messages"] if item["message_type"] == message_type]
    if len(matches) != 1:
        raise ContractError(f"Expected exactly one registry entry for {message_type!r}")
    return matches[0]


@lru_cache(maxsize=None)
def load_schema(message_type: str) -> dict[str, Any]:
    entry = registry_entry(message_type)
    return _read_json(ROOT / entry["schema_path"])


def validate_payload(message_type: str, payload: Any) -> None:
    schema = load_schema(message_type)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def validate_registry_hashes() -> None:
    for item in load_registry()["messages"]:
        for path_key, hash_key in (("schema_path", "schema_hash"), ("example_path", "example_hash")):
            path = ROOT / item[path_key]
            actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != item[hash_key]:
                raise ContractError(f"Hash mismatch for {path.relative_to(ROOT).as_posix()}")


def validate_release_manifest() -> int:
    manifest = _read_json(CONTRACTS_ROOT / "release-manifest.json")
    seen: set[str] = set()
    for item in manifest["files"]:
        if item["path"] in seen:
            raise ContractError(f"Duplicate release manifest path: {item['path']}")
        seen.add(item["path"])
        path = ROOT / item["path"]
        if not path.is_file():
            raise ContractError(f"Missing release artifact: {item['path']}")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["hash"]:
            raise ContractError(f"Release hash mismatch for {item['path']}")
    return len(seen)


def validate_all_examples() -> int:
    validate_registry_hashes()
    count = 0
    for item in load_registry()["messages"]:
        schema = load_schema(item["message_type"])
        Draft202012Validator.check_schema(schema)
        validate_payload(item["message_type"], _read_json(ROOT / item["example_path"]))
        count += 1
    return count


def object_nodes(schema: Any, path: str = "#") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            yield path, schema
        for key, value in schema.items():
            yield from object_nodes(value, f"{path}/{key}")
    elif isinstance(schema, list):
        for index, value in enumerate(schema):
            yield from object_nodes(value, f"{path}/{index}")


def validate_closed_schemas() -> None:
    for item in load_registry()["messages"]:
        for path, node in object_nodes(load_schema(item["message_type"])):
            if node.get("additionalProperties") is not False:
                raise ContractError(f"Open object in {item['message_type']} at {path}")
