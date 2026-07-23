from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from importlib import resources
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    path: str
    code: str
    message: str


class ContractValidationError(ValueError):
    def __init__(self, schema_name: str, issues: list[ValidationIssue]):
        self.schema_name = schema_name
        self.issues = tuple(issues)
        rendered = "; ".join(f"{issue.path}: {issue.code}: {issue.message}" for issue in issues)
        super().__init__(f"{schema_name} validation failed: {rendered}")


class SchemaRegistry:
    def __init__(self, schema_dir: Path | None = None):
        if schema_dir is None:
            root = resources.files("ca_contracts.schemas")
            self._schema_dir = Path(str(root))
        else:
            self._schema_dir = schema_dir
        self._registry = json.loads((self._schema_dir / "CONTRACT_REGISTRY.json").read_text(encoding="utf-8"))
        self._schemas: dict[str, dict[str, Any]] = {}
        for entry in self._registry["schemas"]:
            filename = Path(entry["path"]).name
            self._schemas[filename] = json.loads((self._schema_dir / filename).read_text(encoding="utf-8"))

    @property
    def version(self) -> str:
        return str(self._registry["version"])

    @property
    def schema_names(self) -> tuple[str, ...]:
        return tuple(entry["name"] for entry in self._registry["schemas"])

    def filename_for(self, name: str) -> str:
        normalized = name.removesuffix(".schema.json").replace("-", "_")
        for entry in self._registry["schemas"]:
            if entry["name"] == normalized or entry["title"] == name or Path(entry["path"]).name == name:
                return Path(entry["path"]).name
        raise KeyError(f"unknown contract schema: {name}")

    def schema(self, name: str) -> dict[str, Any]:
        return self._schemas[self.filename_for(name)]

    def validate(self, name: str, payload: Any) -> None:
        filename = self.filename_for(name)
        issues: list[ValidationIssue] = []
        self._validate_node(self._schemas[filename], payload, "$", issues)
        self._validate_cross_field(filename, payload, issues)
        if issues:
            raise ContractValidationError(filename, issues)

    def _resolve(self, node: dict[str, Any]) -> dict[str, Any]:
        if "$ref" not in node:
            return node
        filename = Path(str(node["$ref"])).name
        try:
            return self._schemas[filename]
        except KeyError as error:
            raise KeyError(f"unresolved local schema reference: {filename}") from error

    def _validate_node(
        self,
        node: dict[str, Any],
        value: Any,
        path: str,
        issues: list[ValidationIssue],
    ) -> None:
        if "$ref" in node:
            self._validate_node(self._resolve(node), value, path, issues)
            return
        if "oneOf" in node:
            successes = 0
            candidate_issues: list[list[ValidationIssue]] = []
            for candidate in node["oneOf"]:
                local: list[ValidationIssue] = []
                self._validate_node(candidate, value, path, local)
                candidate_issues.append(local)
                if not local:
                    successes += 1
            if successes != 1:
                issues.append(ValidationIssue(path, "ONE_OF", f"expected exactly one matching branch, got {successes}"))
            return

        expected = node.get("type")
        if isinstance(expected, list):
            if any(self._matches_type(item, value) for item in expected):
                # validate constraints from the matching scalar/object branch
                chosen = next(item for item in expected if self._matches_type(item, value))
                self._validate_node({**node, "type": chosen}, value, path, issues)
                return
            issues.append(ValidationIssue(path, "TYPE", f"expected one of {expected}, got {type(value).__name__}"))
            return

        if expected is not None and not self._matches_type(expected, value):
            issues.append(ValidationIssue(path, "TYPE", f"expected {expected}, got {type(value).__name__}"))
            return

        if "enum" in node and value not in node["enum"]:
            issues.append(ValidationIssue(path, "ENUM", f"value must be one of {node['enum']}"))
            return

        if expected == "object":
            assert isinstance(value, dict)
            required = set(node.get("required", []))
            missing = sorted(required - set(value))
            for field in missing:
                issues.append(ValidationIssue(f"{path}.{field}", "REQUIRED", "required field is missing"))
            properties = node.get("properties", {})
            if node.get("additionalProperties") is False:
                for field in sorted(set(value) - set(properties)):
                    issues.append(ValidationIssue(f"{path}.{field}", "UNKNOWN_FIELD", "unknown governed field"))
            for field, item in value.items():
                if field in properties:
                    self._validate_node(properties[field], item, f"{path}.{field}", issues)
            return

        if expected == "array":
            assert isinstance(value, list)
            if len(value) < int(node.get("minItems", 0)):
                issues.append(ValidationIssue(path, "MIN_ITEMS", f"requires at least {node['minItems']} items"))
            for index, item in enumerate(value):
                self._validate_node(node["items"], item, f"{path}[{index}]", issues)
            if node.get("uniqueItems"):
                fingerprints = [json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False) for item in value]
                if len(fingerprints) != len(set(fingerprints)):
                    issues.append(ValidationIssue(path, "UNIQUE_ITEMS", "array items must be unique"))
            return

        if expected == "string":
            assert isinstance(value, str)
            if len(value) < int(node.get("minLength", 0)):
                issues.append(ValidationIssue(path, "MIN_LENGTH", f"minimum length is {node['minLength']}"))
            pattern = node.get("pattern")
            if pattern and not re.fullmatch(pattern, value):
                issues.append(ValidationIssue(path, "PATTERN", f"value does not match {pattern}"))
            if node.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(ValidationIssue(path, "DATE_TIME", "invalid RFC 3339 timestamp"))
            return

        if expected == "integer":
            assert isinstance(value, int) and not isinstance(value, bool)
            if "minimum" in node and value < int(node["minimum"]):
                issues.append(ValidationIssue(path, "MINIMUM", f"value must be >= {node['minimum']}"))
            return

    @staticmethod
    def _matches_type(expected: str, value: Any) -> bool:
        return {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "boolean": isinstance(value, bool),
            "null": value is None,
        }.get(expected, False)

    @staticmethod
    def _validate_cross_field(filename: str, payload: Any, issues: list[ValidationIssue]) -> None:
        if not isinstance(payload, dict):
            return
        if filename == "source-span-ref.schema.json":
            start = payload.get("start_ms")
            end = payload.get("end_ms")
            if isinstance(start, int) and isinstance(end, int) and end <= start:
                issues.append(ValidationIssue("$.end_ms", "SPAN_ORDER", "end_ms must be greater than start_ms"))
        if filename == "receipt-envelope.schema.json":
            outcome = payload.get("outcome")
            failure = payload.get("failure")
            if outcome in {"denied", "failed"} and failure is None:
                issues.append(ValidationIssue("$.failure", "FAILURE_REQUIRED", "denied or failed receipt requires failure"))
            if outcome in {"accepted", "cancelled"} and failure is not None:
                issues.append(ValidationIssue("$.failure", "FAILURE_FORBIDDEN", "accepted or cancelled receipt cannot contain failure"))


_DEFAULT_REGISTRY: SchemaRegistry | None = None


def registry() -> SchemaRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        _DEFAULT_REGISTRY = SchemaRegistry()
    return _DEFAULT_REGISTRY


def validate_payload(schema_name: str, payload: Any) -> None:
    registry().validate(schema_name, payload)
