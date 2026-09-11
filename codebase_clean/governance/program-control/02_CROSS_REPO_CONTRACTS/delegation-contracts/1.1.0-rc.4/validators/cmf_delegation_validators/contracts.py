"""Schema, registry, and example validation."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator, FormatChecker

from .paths import CONTRACTS_ROOT, LAYOUT, ROOT, distribution_path


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
    return _read_json(distribution_path(entry["schema_path"]))


def validate_payload(message_type: str, payload: Any) -> None:
    schema = load_schema(message_type)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def validate_registry_hashes() -> None:
    for item in load_registry()["messages"]:
        for path_key, hash_key in (("schema_path", "schema_hash"), ("example_path", "example_hash")):
            path = distribution_path(item[path_key])
            actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != item[hash_key]:
                raise ContractError(f"Hash mismatch for {path.relative_to(ROOT).as_posix()}")


def _is_transient(relative_path: str) -> bool:
    path = Path(relative_path)
    return (
        bool({".pytest_cache", "__pycache__"}.intersection(path.parts))
        or path.name in {".DS_Store", "Thumbs.db", "desktop.ini"}
        or path.suffix.lower() in {".pyc", ".pyo", ".tmp", ".temp", ".swp", ".swo"}
        or path.name.endswith("~")
    )


def _validate_inventory(
    manifest: dict[str, Any], *, hash_key: str, excluded_paths: set[str]
) -> int:
    seen: set[str] = set()
    for item in manifest["files"]:
        relative_path = item["path"]
        if relative_path in seen:
            raise ContractError(f"Duplicate manifest path: {relative_path}")
        if _is_transient(relative_path):
            raise ContractError(f"Transient artifact is forbidden in manifest: {relative_path}")
        seen.add(relative_path)
        path = distribution_path(relative_path)
        if not path.is_file():
            raise ContractError(f"Missing distribution artifact: {relative_path}")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item[hash_key]:
            raise ContractError(f"Manifest hash mismatch for {relative_path}")
        if "bytes" in item and path.stat().st_size != item["bytes"]:
            raise ContractError(f"Manifest byte count mismatch for {relative_path}")

    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in excluded_paths
        and not _is_transient(path.relative_to(ROOT).as_posix())
    }
    if seen != actual_paths:
        missing = sorted(actual_paths - seen)
        extra = sorted(seen - actual_paths)
        raise ContractError(f"Manifest inventory mismatch: unlisted={missing}, missing={extra}")
    return len(seen)


def validate_source_manifest() -> int:
    manifest = _read_json(CONTRACTS_ROOT / "source-manifest.json")
    if manifest.get("status") != "SOURCE_ONLY" or manifest.get("required_for_release_validation"):
        raise ContractError("Source manifest must be explicitly non-release")
    return _validate_inventory(
        manifest,
        hash_key="sha256",
        excluded_paths={"contracts/source-manifest.json", "contracts/release-manifest.json"},
    )


def validate_release_manifest() -> int:
    if LAYOUT == "SOURCE":
        return validate_source_manifest()
    manifest = _read_json(CONTRACTS_ROOT / "release-manifest.json")
    if manifest.get("layout") != "release-root-relative":
        raise ContractError("Release manifest is not release-root-relative")
    if manifest.get("generation_basis") != "actual_release_directory":
        raise ContractError("Release manifest was not generated from release contents")
    if manifest.get("self_path") != "contracts/release-manifest.json":
        raise ContractError("Release manifest self path is not explicit")
    if manifest.get("receipt_path") != "RELEASE_RECEIPT.json":
        raise ContractError("Release receipt path is not explicit")
    return _validate_inventory(
        manifest,
        hash_key="sha256",
        excluded_paths={"contracts/release-manifest.json", "RELEASE_RECEIPT.json"},
    )


def validate_release_receipt() -> int:
    if LAYOUT != "RELEASE":
        raise ContractError("Release receipt validation requires a release layout")
    receipt_path = ROOT / "RELEASE_RECEIPT.json"
    receipt = _read_json(receipt_path)
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for item in receipt.get("files", []):
        relative_path = item["path"]
        if relative_path in seen:
            raise ContractError(f"Duplicate receipt path: {relative_path}")
        if _is_transient(relative_path):
            raise ContractError(f"Transient artifact is forbidden in receipt: {relative_path}")
        seen.add(relative_path)
        path = distribution_path(relative_path)
        if not path.is_file():
            raise ContractError(f"Receipt artifact is missing: {relative_path}")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise ContractError(f"Receipt mismatch for {relative_path}")
        normalized.append(item)
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix() != "RELEASE_RECEIPT.json"
        and not _is_transient(path.relative_to(ROOT).as_posix())
    }
    if seen != actual_paths:
        raise ContractError("Receipt inventory does not exactly match release contents")
    digest_input = json.dumps(
        normalized, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    release_digest = "sha256:" + hashlib.sha256(digest_input).hexdigest()
    if release_digest != receipt.get("release_digest"):
        raise ContractError("Release digest mismatch")
    manifest_hash = "sha256:" + hashlib.sha256(
        (CONTRACTS_ROOT / "release-manifest.json").read_bytes()
    ).hexdigest()
    if manifest_hash != receipt.get("release_manifest_sha256"):
        raise ContractError("Receipt release manifest hash mismatch")
    if receipt.get("file_count_excluding_receipt") != len(seen):
        raise ContractError("Receipt file count mismatch")
    return len(seen)


def validate_all_examples() -> int:
    validate_registry_hashes()
    count = 0
    for item in load_registry()["messages"]:
        schema = load_schema(item["message_type"])
        Draft202012Validator.check_schema(schema)
        validate_payload(item["message_type"], _read_json(distribution_path(item["example_path"])))
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
